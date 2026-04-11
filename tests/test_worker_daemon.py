from __future__ import annotations

from io import BytesIO
from urllib.error import HTTPError

import pytest

from ollama_network.worker_daemon import WorkerConfig, WorkerDaemon


def _build_worker_daemon() -> WorkerDaemon:
    return WorkerDaemon(
        WorkerConfig(
            server_url="https://example.com",
            worker_id="worker-a",
            owner_user_id="user-a",
            gpu_name="RTX 4090",
            vram_gb=24.0,
            installed_models=("llama3.1:8b",),
            benchmark_tokens_per_second={"llama3.1:8b": 70.0},
        )
    )


def test_worker_daemon_formats_cloudflare_1010_as_reachability_issue(monkeypatch) -> None:
    daemon = _build_worker_daemon()

    def fake_urlopen(*_args, **_kwargs):
        raise HTTPError(
            url="https://example.com/workers/register",
            code=403,
            msg="Forbidden",
            hdrs=None,
            fp=BytesIO(b"error code: 1010"),
        )

    monkeypatch.setattr("ollama_network.worker_daemon.request.urlopen", fake_urlopen)

    with pytest.raises(RuntimeError) as exc_info:
        daemon._post("/workers/register", {})

    message = str(exc_info.value)
    assert "403" in message
    assert "1010" in message
    assert "Cloudflare" in message or "blocked this worker's request" in message


def test_worker_daemon_keeps_other_http_errors_short(monkeypatch) -> None:
    daemon = _build_worker_daemon()

    def fake_urlopen(*_args, **_kwargs):
        raise HTTPError(
            url="https://example.com/workers/register",
            code=500,
            msg="Internal Server Error",
            hdrs=None,
            fp=BytesIO(b"upstream exploded"),
        )

    monkeypatch.setattr("ollama_network.worker_daemon.request.urlopen", fake_urlopen)

    with pytest.raises(RuntimeError) as exc_info:
        daemon._post("/workers/register", {})

    message = str(exc_info.value)
    assert "500" in message
    assert "upstream exploded" in message

