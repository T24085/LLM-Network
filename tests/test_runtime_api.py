import json
import threading
import time
from urllib import request

from ollama_network.api import NetworkHTTPServer
from ollama_network.local_hardware import LocalGPUDevice, LocalHardwareDetection
from ollama_network.ollama_local import LocalModelDetection
from ollama_network.models import ExecutorResult
from ollama_network.service import NetworkService
from ollama_network.state_store import LocalStateStore
from ollama_network.worker_daemon import WorkerConfig, WorkerDaemon


class FakeExecutor:
    def __init__(self, output_text: str = "completed from fake executor") -> None:
        self.output_text = output_text

    def run(self, model_tag: str, prompt: str, max_output_tokens: int) -> ExecutorResult:
        return ExecutorResult(
            success=True,
            output_text=f"{self.output_text}: {model_tag}",
            output_tokens=48,
            latency_seconds=0.01,
            verified=True,
        )


class FakeModelDetector:
    def __init__(self, models: list[str], available: bool = True, error: str = "") -> None:
        self._result = LocalModelDetection(
            ollama_available=available,
            models=models,
            error=error,
        )

    def detect(self) -> LocalModelDetection:
        return self._result


class FakeHardwareDetector:
    def detect(self) -> LocalHardwareDetection:
        return LocalHardwareDetection(
            detected=True,
            primary_gpu_name="RTX 4090",
            primary_vram_gb=24.0,
            gpus=[LocalGPUDevice(name="RTX 4090", vram_gb=24.0, source="fake")],
            error="",
        )


def api_post(base_url: str, path: str, payload: dict[str, object]) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=f"{base_url}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def api_get(base_url: str, path: str) -> dict[str, object]:
    with request.urlopen(f"{base_url}{path}", timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def text_get(base_url: str, path: str) -> str:
    with request.urlopen(f"{base_url}{path}", timeout=10) as response:
        return response.read().decode("utf-8")


def test_worker_daemon_executes_claimed_job_end_to_end(tmp_path) -> None:
    service = NetworkService(
        executor_factory=lambda _worker_id: FakeExecutor(),
        state_store=LocalStateStore(tmp_path / "private_state.json"),
    )
    server = NetworkHTTPServer(("127.0.0.1", 0), service=service)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"

    try:
        api_post(base_url, "/users/register", {"user_id": "alice", "starting_credits": 5.0})
        issued = api_post(base_url, "/users/issue", {"starting_credits": 1.5})
        assert issued["user_id"].startswith("usr_")
        worker = WorkerDaemon(
            config=WorkerConfig(
                server_url=base_url,
                worker_id="worker-bob",
                owner_user_id="bob",
                gpu_name="RTX 4090",
                vram_gb=24.0,
                installed_models=("llama3.1:8b",),
                benchmark_tokens_per_second={"llama3.1:8b": 72.0},
            ),
            executor=FakeExecutor(),
        )
        worker.register()

        created = api_post(
            base_url,
            "/jobs",
            {
                "requester_user_id": "alice",
                "model_tag": "llama3.1:8b",
                "prompt": "Write a concise network design note.",
                "max_output_tokens": 300,
                "prompt_tokens": 20,
            },
        )

        completed = worker.run_once()
        assert completed is not None
        assert completed["status"] == "completed"
        assert completed["assigned_worker_id"] == "worker-bob"
        assert completed["result"]["output_text"].startswith("completed from fake executor")

        fetched = api_get(base_url, f"/jobs/{created['job_id']}")
        assert fetched["status"] == "completed"

        network = api_get(base_url, "/network")
        assert network["user_count"] == 3
        assert network["privacy"]["balances_exposed"] is False
        assert api_get(base_url, "/users/bob")["balance"] > 0
        assert api_get(base_url, "/users/alice")["balance"] < 5.0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_dashboard_and_local_worker_cycle_routes(tmp_path) -> None:
    service = NetworkService(
        executor_factory=lambda _worker_id: FakeExecutor("ui executor"),
        model_detector=FakeModelDetector(models=["llama3.1:8b", "qwen3:4b"]),
        hardware_detector=FakeHardwareDetector(),
        state_store=LocalStateStore(tmp_path / "private_state.json"),
    )
    server = NetworkHTTPServer(("127.0.0.1", 0), service=service)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"

    try:
        html = text_get(base_url, "/dashboard")
        assert "LLM Network Control Room" in html
        models = api_get(base_url, "/models")
        assert any(model["tag"] == "llama3.1:8b" for model in models["models"])
        assert models["local_detection"]["approved_local_models"] == ["llama3.1:8b", "qwen3:4b"]
        assert models["local_detection"]["unapproved_local_models"] == []
        worker_context = api_get(base_url, "/worker-context")
        assert worker_context["suggested_gpu_name"] == "RTX 4090"
        assert worker_context["suggested_vram_gb"] == 24.0
        assert worker_context["suggested_installed_models"] == ["llama3.1:8b", "qwen3:4b"]
        assert worker_context["suggested_benchmark_tokens_per_second"]["llama3.1:8b"] > 0

        issued = api_post(base_url, "/users/issue", {"starting_credits": 6.0})
        assert issued["user_id"].startswith("usr_")

        started = api_post(
            base_url,
            "/workers/start-local",
            {
                "worker_id": "worker-bob",
                "owner_user_id": "bob",
                "gpu_name": "RTX 4090",
                "vram_gb": 24,
                "installed_models": ["llama3.1:8b"],
                "benchmark_tokens_per_second": {"llama3.1:8b": 72},
                "poll_interval_seconds": 0.05,
                "runtime": "ollama",
                "allows_cloud_fallback": False,
            },
        )
        assert started["loop"]["running"] is True
        api_post(
            base_url,
            "/jobs",
            {
                "requester_user_id": issued["user_id"],
                "model_tag": "llama3.1:8b",
                "prompt": "Generate a design memo.",
                "max_output_tokens": 200,
                "prompt_tokens": 20,
            },
        )

        completed_job = None
        for _ in range(40):
            network = api_get(base_url, "/network")
            local_loop = network["local_workers"]["worker-bob"]
            if local_loop["jobs_completed"] >= 1:
                completed_job = local_loop
                break
            time.sleep(0.05)
        assert completed_job is not None

        user = api_get(base_url, "/users/bob")
        assert user["balance"] > 0

        stopped = api_post(base_url, "/workers/worker-bob/stop-local", {})
        assert stopped["loop"]["running"] is False

        missing_error = None
        try:
            api_get(base_url, "/users/unknown_user")
        except Exception as error:
            missing_error = error
        assert missing_error is not None
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
