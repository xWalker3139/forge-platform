import os
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

import pytest


@pytest.mark.skipif(sys.platform == "win32", reason="SIGTERM lifecycle is verified on Linux")
def test_real_server_and_shutdown(tmp_path):
    # Run in the same test process network namespace; do not depend on another terminal.
    log = tmp_path / "server.log"
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    with log.open("w+") as output:
        process = subprocess.Popen(
            [sys.executable, "-c", "from forge_service.main import run; run()"],
            env=dict(os.environ, PYTHONPATH="src", PORT=str(port)),
            stdout=output,
            stderr=output,
        )
        try:
            for _ in range(100):
                if process.poll() is not None:
                    raise AssertionError(log.read_text())
                try:
                    with urllib.request.urlopen(base + "/health/ready", timeout=1) as r:
                        assert r.status == 200
                    break
                except urllib.error.URLError:
                    time.sleep(0.05)
            else:
                raise AssertionError("server did not become ready")
            for _ in range(20):
                with urllib.request.urlopen(base + "/api/greeting", timeout=2) as r:
                    assert r.status == 200
            process.terminate()
            # Uvicorn restores and re-raises the original signal after graceful cleanup.
            assert process.wait(timeout=10) in (0, -signal.SIGTERM)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
    assert "Application shutdown complete" in log.read_text()
