from __future__ import annotations

from ollama_network.local_hardware import LocalGPUDevice, LocalHardwareDetection
from ollama_network.ollama_local import LocalModelDetection
from ollama_network.worker_bootstrap import (
    WorkerBootstrapProfile,
    build_profile,
    load_profile,
    save_profile,
)


class FakeHardwareDetector:
    def __init__(self, detection: LocalHardwareDetection) -> None:
        self._detection = detection

    def detect(self) -> LocalHardwareDetection:
        return self._detection


class FakeModelDetector:
    def __init__(self, detection: LocalModelDetection) -> None:
        self._detection = detection

    def detect(self) -> LocalModelDetection:
        return self._detection


class EmptyHardwareDetector:
    def detect(self) -> LocalHardwareDetection:
        return LocalHardwareDetection(
            detected=False,
            primary_gpu_name="",
            primary_vram_gb=0.0,
            system_ram_gb=0.0,
            gpus=[],
            error="no gpu",
        )


class EmptyModelDetector:
    def detect(self) -> LocalModelDetection:
        return LocalModelDetection(
            ollama_available=False,
            models=[],
            error="ollama missing",
        )


def test_worker_bootstrap_saves_profile_for_future_launches(tmp_path) -> None:
    config_path = tmp_path / ".runtime" / "worker.local.json"
    detection = LocalHardwareDetection(
        detected=True,
        primary_gpu_name="RTX 4090",
        primary_vram_gb=24.0,
        system_ram_gb=32.0,
        gpus=[LocalGPUDevice(name="RTX 4090", vram_gb=24.0, source="fake")],
        error="",
    )
    models = LocalModelDetection(
        ollama_available=True,
        models=["llama3.1:8b", "qwen3:4b"],
        error="",
    )

    profile = build_profile(
        config_path=config_path,
        hardware_detector=FakeHardwareDetector(detection),
        model_detector=FakeModelDetector(models),
        worker_id="worker-bob",
        owner_user_id="bob",
        worker_token="worker-token-123",
        server_url="http://127.0.0.1:8000",
        no_prompt=True,
    )
    save_profile(config_path, profile)

    saved = load_profile(config_path)
    assert saved["owner_user_id"] == "bob"
    assert saved["worker_token"] == "worker-token-123"
    assert saved["gpu_name"] == "RTX 4090"
    assert saved["installed_models"] == ["llama3.1:8b", "qwen3:4b"]


def test_worker_bootstrap_reuses_cached_profile_without_prompt(tmp_path) -> None:
    config_path = tmp_path / ".runtime" / "worker.local.json"
    save_profile(
        config_path,
        WorkerBootstrapProfile(
            server_url="http://127.0.0.1:8000",
            worker_id="worker-bob",
            owner_user_id="bob",
            worker_token="worker-token-123",
            firebase_id_token="firebase-token",
            gpu_name="RTX 4090",
            vram_gb=24.0,
            installed_models=("llama3.1:8b", "qwen3:4b"),
            benchmark_tokens_per_second={"llama3.1:8b": 72.0, "qwen3:4b": 55.0},
        ),
    )

    profile = build_profile(
        config_path=config_path,
        hardware_detector=EmptyHardwareDetector(),
        model_detector=EmptyModelDetector(),
        no_prompt=True,
    )

    assert profile.server_url == "http://127.0.0.1:8000"
    assert profile.worker_id == "worker-bob"
    assert profile.owner_user_id == "bob"
    assert profile.worker_token == "worker-token-123"
    assert profile.gpu_name == "RTX 4090"
    assert profile.vram_gb == 24.0
    assert profile.installed_models == ("llama3.1:8b", "qwen3:4b")
    assert profile.benchmark_tokens_per_second["llama3.1:8b"] == 72.0
