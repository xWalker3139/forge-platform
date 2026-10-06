from fastapi.testclient import TestClient

from forge_service.main import create_app


def test_health_lifecycle():
    app = create_app()
    assert not app.state.ready
    with TestClient(app) as client:
        assert client.get("/health/live").status_code == 200
        assert client.get("/health/ready").status_code == 200
    assert not app.state.ready


def test_version():
    with TestClient(create_app()) as client:
        assert client.get("/version").json()["version"] == "0.1.0"


def test_docs():
    with TestClient(create_app()) as client:
        assert client.get("/docs").status_code == 200


def test_request_id():
    with TestClient(create_app()) as client:
        assert (
            client.get("/version", headers={"X-Request-ID": "test-123"}).headers["X-Request-ID"]
            == "test-123"
        )
        assert (
            client.get("/version", headers={"X-Request-ID": "invalid value"}).headers[
                "X-Request-ID"
            ]
            != "invalid value"
        )


def test_metrics_bounded_labels():
    with TestClient(create_app()) as client:
        client.get("/api/greeting")
        client.get("/unknown/12345")
        metrics = client.get("/metrics").text
        assert 'route="/api/greeting"' in metrics
        assert 'route="unmatched"' in metrics
        assert "/unknown/12345" not in metrics


def test_faults_disabled():
    with TestClient(create_app()) as client:
        assert client.get("/internal/simulate/error").status_code == 404


def test_faults_enabled(monkeypatch):
    monkeypatch.setenv("ENABLE_FAULTS", "true")
    with TestClient(create_app()) as client:
        assert client.get("/internal/simulate/error").status_code == 503
        assert client.get("/internal/simulate/latency?milliseconds=1").status_code == 200
        assert client.get("/internal/simulate/latency?milliseconds=5000").status_code == 422
