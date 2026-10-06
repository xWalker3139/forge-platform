import asyncio
import json
import os
import re
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import Response
from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, generate_latest


def create_app():
    registry = CollectorRegistry()
    requests = Counter(
        "forge_http_requests_total",
        "Completed requests",
        ["method", "route", "status"],
        registry=registry,
    )
    latency = Histogram(
        "forge_http_request_duration_seconds", "Request duration", ["route"], registry=registry
    )
    active = Gauge("forge_http_requests_in_progress", "Active requests", registry=registry)
    version = os.getenv("APP_VERSION", "0.1.0")
    build = Gauge("forge_build_info", "Build metadata", ["version", "commit"], registry=registry)
    build.labels(version, os.getenv("GIT_SHA", "local")).set(1)
    faults = os.getenv("ENABLE_FAULTS", "false").lower() == "true"

    @asynccontextmanager
    async def lifespan(app):
        app.state.ready = True
        yield
        app.state.ready = False

    app = FastAPI(
        title=os.getenv("SERVICE_NAME", "Forge Reference Service"),
        version=version,
        lifespan=lifespan,
    )
    app.state.ready = False

    @app.middleware("http")
    async def telemetry(request: Request, call_next):
        incoming = request.headers.get("X-Request-ID", "")
        request_id = (
            incoming if re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", incoming) else uuid.uuid4().hex
        )
        start = time.monotonic()
        status = 500
        active.inc()
        try:
            response = await call_next(request)
            status = response.status_code
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            route = getattr(request.scope.get("route"), "path", "unmatched")
            duration = time.monotonic() - start
            if route not in ("/metrics", "/health/live", "/health/ready"):
                requests.labels(request.method, route, str(status)).inc()
                latency.labels(route).observe(duration)
            active.dec()
            print(
                json.dumps(
                    {
                        "request_id": request_id,
                        "route": route,
                        "status": status,
                        "duration_ms": round(duration * 1000, 2),
                    }
                ),
                flush=True,
            )

    @app.get("/health/live")
    async def live():
        return {"status": "alive"}

    @app.get("/health/ready")
    async def ready():
        if not app.state.ready:
            raise HTTPException(503, "not_ready")
        return {"status": "ready"}

    @app.get("/version")
    async def info():
        return {"version": version, "commit": os.getenv("GIT_SHA", "local")}

    @app.get("/api/greeting")
    async def greeting():
        return {"message": "Hello from Forge", "version": version}

    @app.get("/metrics", include_in_schema=False)
    async def metrics():
        return Response(generate_latest(registry), media_type="text/plain; version=0.0.4")

    @app.get("/internal/simulate/latency")
    async def slow(milliseconds: int = Query(100, ge=0, le=2000)):
        if not faults:
            raise HTTPException(404, "disabled")
        await asyncio.sleep(milliseconds / 1000)
        return {"delay_ms": milliseconds}

    @app.get("/internal/simulate/error")
    async def error():
        if not faults:
            raise HTTPException(404, "disabled")
        raise HTTPException(503, "simulated_failure")

    return app


app = create_app()


def run():
    import uvicorn

    uvicorn.run(
        "forge_service.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        timeout_graceful_shutdown=20,
        access_log=False,
    )
