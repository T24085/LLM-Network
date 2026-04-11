from __future__ import annotations

import argparse
import json
import os
import socket
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .local_hardware import LocalHardwareDetector
from .ollama_local import LocalOllamaModelDetector
from .worker_daemon import WorkerConfig, WorkerDaemon


DEFAULT_SERVER_URL = "https://llm-network.websitesolutions.shop"
DEFAULT_POLL_INTERVAL_SECONDS = 2.0
DEFAULT_MAX_CONCURRENT_JOBS = 1


@dataclass(frozen=True)
class WorkerBootstrapProfile:
    server_url: str = DEFAULT_SERVER_URL
    worker_id: str = ""
    owner_user_id: str = ""
    worker_token: str = ""
    firebase_id_token: str = ""
    gpu_name: str = ""
    vram_gb: float = 0.0
    installed_models: tuple[str, ...] = ()
    benchmark_tokens_per_second: dict[str, float] = field(default_factory=dict)
    poll_interval_seconds: float = DEFAULT_POLL_INTERVAL_SECONDS
    max_concurrent_jobs: int = DEFAULT_MAX_CONCURRENT_JOBS


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_profile_path(root: Optional[Path] = None) -> Path:
    return (root or project_root()) / ".runtime" / "worker.local.json"


def load_profile(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def save_profile(path: Path, profile: WorkerBootstrapProfile) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "server_url": profile.server_url,
        "worker_id": profile.worker_id,
        "owner_user_id": profile.owner_user_id,
        "worker_token": profile.worker_token,
        "firebase_id_token": profile.firebase_id_token,
        "gpu_name": profile.gpu_name,
        "vram_gb": profile.vram_gb,
        "installed_models": list(profile.installed_models),
        "benchmark_tokens_per_second": profile.benchmark_tokens_per_second,
        "poll_interval_seconds": profile.poll_interval_seconds,
        "max_concurrent_jobs": profile.max_concurrent_jobs,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _prompt_value(prompt: str, default: str = "", required: bool = False) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{prompt}{suffix}: ").strip()
        if value:
            return value
        if default:
            return default
        if not required:
            return ""
        print("This value is required.")


def _prompt_models(default_models: list[str]) -> list[str]:
    default_text = ", ".join(default_models)
    value = _prompt_value(
        "Enter the Ollama model tags this worker should advertise (comma-separated)",
        default=default_text,
        required=True,
    )
    return [item.strip() for item in value.split(",") if item.strip()]


def _prompt_float(prompt: str, default: float, required: bool = False) -> float:
    fallback = f"{default:g}" if default > 0 else ""
    while True:
        raw = _prompt_value(prompt, default=fallback, required=required)
        if not raw:
            return default
        try:
            return float(raw)
        except ValueError:
            print("Enter a numeric value.")


def _coerce_float(value: object, default: float) -> float:
    if value in ("", None):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_int(value: object, default: int) -> int:
    if value in ("", None):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _resolve_worker_id(config: dict[str, object], override: Optional[str]) -> str:
    if override:
        return override
    cached = str(config.get("worker_id", "")).strip()
    if cached:
        return cached
    return f"worker-{socket.gethostname().upper()}"


def _resolve_owner_user_id(config: dict[str, object], override: Optional[str], no_prompt: bool) -> str:
    if override:
        return override.strip()
    cached = str(config.get("owner_user_id", "")).strip()
    if cached:
        return cached
    if no_prompt:
        return ""
    return _prompt_value("Enter the network user id that owns this worker", required=True)


def _resolve_worker_token(config: dict[str, object], override: Optional[str], no_prompt: bool) -> str:
    if override:
        return override.strip()
    cached = str(config.get("worker_token", "")).strip()
    if cached:
        return cached
    if no_prompt:
        return ""
    print()
    print("Paste the long-lived worker token for this PC.")
    print("This token is required to register and claim jobs from the coordinator.")
    return _prompt_value("Worker token", required=True)


def _detect_worker_profile(
    config: dict[str, object],
    hardware_detector: Optional[object] = None,
    model_detector: Optional[object] = None,
) -> tuple[str, float, list[str], dict[str, float]]:
    hardware = (hardware_detector or LocalHardwareDetector()).detect()
    model_detection = (model_detector or LocalOllamaModelDetector()).detect()

    cached_models = [
        str(item).strip()
        for item in config.get("installed_models", [])
        if str(item).strip()
    ]
    cached_throughput = {
        str(key): float(value)
        for key, value in dict(config.get("benchmark_tokens_per_second", {})).items()
    }

    gpu_name = hardware.primary_gpu_name or str(config.get("gpu_name", "")).strip()
    vram_gb = hardware.primary_vram_gb or float(config.get("vram_gb", 0.0) or 0.0)

    installed_models = list(model_detection.models) if model_detection.ollama_available and model_detection.models else cached_models
    benchmark_tokens_per_second = dict(cached_throughput)
    for model_tag in installed_models:
        benchmark_tokens_per_second.setdefault(model_tag, 1.0)

    return gpu_name, vram_gb, installed_models, benchmark_tokens_per_second


def build_profile(
    *,
    config_path: Optional[Path] = None,
    hardware_detector: Optional[object] = None,
    model_detector: Optional[object] = None,
    worker_id: Optional[str] = None,
    owner_user_id: Optional[str] = None,
    worker_token: Optional[str] = None,
    server_url: Optional[str] = None,
    firebase_id_token: Optional[str] = None,
    poll_interval_seconds: Optional[float] = None,
    max_concurrent_jobs: Optional[int] = None,
    no_prompt: bool = False,
) -> WorkerBootstrapProfile:
    path = config_path or default_profile_path()
    config = load_profile(path)
    env = os.environ

    resolved_server_url = (
        (server_url or "").strip()
        or env.get("OLLAMA_NETWORK_SERVER_URL", "").strip()
        or str(config.get("server_url", "")).strip()
        or DEFAULT_SERVER_URL
    )
    resolved_worker_id = _resolve_worker_id(config, worker_id or env.get("OLLAMA_NETWORK_WORKER_ID"))
    resolved_owner_user_id = _resolve_owner_user_id(
        config,
        owner_user_id or env.get("OLLAMA_NETWORK_OWNER_USER_ID"),
        no_prompt=no_prompt,
    )
    resolved_worker_token = _resolve_worker_token(
        config,
        worker_token or env.get("OLLAMA_NETWORK_WORKER_TOKEN"),
        no_prompt=no_prompt,
    )
    resolved_firebase_id_token = (
        (firebase_id_token or "").strip()
        or env.get("OLLAMA_NETWORK_FIREBASE_ID_TOKEN", "").strip()
        or str(config.get("firebase_id_token", "")).strip()
    )
    detected_gpu_name, detected_vram_gb, detected_models, detected_throughput = _detect_worker_profile(
        config,
        hardware_detector=hardware_detector,
        model_detector=model_detector,
    )

    if not detected_gpu_name and not no_prompt:
        print()
        print("Could not auto-detect the GPU for this worker.")
        detected_gpu_name = _prompt_value("GPU name", default=str(config.get("gpu_name", "")).strip(), required=True)
    if not detected_gpu_name and no_prompt:
        raise ValueError("Unable to determine the GPU name for this worker.")
    if detected_vram_gb <= 0 and not no_prompt:
        detected_vram_gb = _prompt_float("Dedicated VRAM in GB", float(config.get("vram_gb", 0.0) or 0.0), required=True)
    if detected_vram_gb <= 0 and no_prompt:
        raise ValueError("Unable to determine the dedicated VRAM for this worker.")

    if not detected_models:
        if no_prompt:
            detected_models = [
                str(item).strip()
                for item in config.get("installed_models", [])
                if str(item).strip()
            ]
        else:
            detected_models = _prompt_models(
                [
                    str(item).strip()
                    for item in config.get("installed_models", [])
                    if str(item).strip()
                ]
            )
    if not detected_models:
        raise ValueError("At least one Ollama model tag is required for the worker.")

    if not resolved_owner_user_id:
        raise ValueError("owner_user_id is required.")
    if not resolved_worker_token:
        raise ValueError("worker_token is required.")

    poll_interval = _coerce_float(
        poll_interval_seconds
        if poll_interval_seconds is not None
        else env.get("OLLAMA_NETWORK_WORKER_POLL_INTERVAL", "")
        or config.get("poll_interval_seconds", DEFAULT_POLL_INTERVAL_SECONDS),
        DEFAULT_POLL_INTERVAL_SECONDS,
    )
    max_jobs = _coerce_int(
        max_concurrent_jobs
        if max_concurrent_jobs is not None
        else env.get("OLLAMA_NETWORK_WORKER_MAX_CONCURRENT_JOBS", "")
        or config.get("max_concurrent_jobs", DEFAULT_MAX_CONCURRENT_JOBS),
        DEFAULT_MAX_CONCURRENT_JOBS,
    )

    profile = WorkerBootstrapProfile(
        server_url=resolved_server_url,
        worker_id=resolved_worker_id,
        owner_user_id=resolved_owner_user_id,
        worker_token=resolved_worker_token,
        firebase_id_token=resolved_firebase_id_token,
        gpu_name=detected_gpu_name,
        vram_gb=float(detected_vram_gb),
        installed_models=tuple(detected_models),
        benchmark_tokens_per_second={
            **detected_throughput,
            **{
                model_tag: detected_throughput.get(model_tag, 1.0)
                for model_tag in detected_models
            },
        },
        poll_interval_seconds=poll_interval,
        max_concurrent_jobs=max_jobs,
    )
    return profile


def launch_worker(
    *,
    config_path: Optional[Path] = None,
    hardware_detector: Optional[object] = None,
    model_detector: Optional[object] = None,
    worker_id: Optional[str] = None,
    owner_user_id: Optional[str] = None,
    worker_token: Optional[str] = None,
    server_url: Optional[str] = None,
    firebase_id_token: Optional[str] = None,
    poll_interval_seconds: Optional[float] = None,
    max_concurrent_jobs: Optional[int] = None,
    no_prompt: bool = False,
    write_config_only: bool = False,
) -> WorkerBootstrapProfile:
    path = config_path or default_profile_path()
    profile = build_profile(
        config_path=path,
        hardware_detector=hardware_detector,
        model_detector=model_detector,
        worker_id=worker_id,
        owner_user_id=owner_user_id,
        worker_token=worker_token,
        server_url=server_url,
        firebase_id_token=firebase_id_token,
        poll_interval_seconds=poll_interval_seconds,
        max_concurrent_jobs=max_concurrent_jobs,
        no_prompt=no_prompt,
    )
    save_profile(path, profile)
    if write_config_only:
        print(f"Saved worker bootstrap profile to {path}")
        return profile

    config = WorkerConfig(
        server_url=profile.server_url,
        worker_id=profile.worker_id,
        owner_user_id=profile.owner_user_id,
        gpu_name=profile.gpu_name,
        vram_gb=profile.vram_gb,
        installed_models=profile.installed_models,
        benchmark_tokens_per_second=profile.benchmark_tokens_per_second,
        poll_interval_seconds=profile.poll_interval_seconds,
        max_concurrent_jobs=profile.max_concurrent_jobs,
        worker_token=profile.worker_token,
        firebase_id_token=profile.firebase_id_token,
    )
    print(
        f"Worker {profile.worker_id} serving {', '.join(profile.installed_models) or 'no models'} "
        f"via {profile.server_url}"
    )
    WorkerDaemon(config=config).serve_forever()
    return profile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bootstrap and run an Ollama Network worker daemon.")
    parser.add_argument("--config-path", default="", help="Optional worker bootstrap profile path.")
    parser.add_argument("--server-url", default="", help="Coordinator API URL override.")
    parser.add_argument("--worker-id", default="", help="Stable worker identifier override.")
    parser.add_argument("--owner-user-id", default="", help="User id that earns credits.")
    parser.add_argument("--worker-token", default="", help="Long-lived worker token for this PC.")
    parser.add_argument("--firebase-id-token", default="", help="Optional Firebase ID token override.")
    parser.add_argument("--poll-interval", type=float, default=None, help="Poll interval in seconds.")
    parser.add_argument("--max-concurrent-jobs", type=int, default=None, help="Maximum active jobs.")
    parser.add_argument("--no-prompt", action="store_true", help="Fail if required worker settings are missing.")
    parser.add_argument(
        "--write-config-only",
        action="store_true",
        help="Save the worker bootstrap profile without starting the daemon.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    config_path = Path(args.config_path) if args.config_path else None
    launch_worker(
        config_path=config_path,
        worker_id=args.worker_id or None,
        owner_user_id=args.owner_user_id or None,
        worker_token=args.worker_token or None,
        server_url=args.server_url or None,
        firebase_id_token=args.firebase_id_token or None,
        poll_interval_seconds=args.poll_interval,
        max_concurrent_jobs=args.max_concurrent_jobs,
        no_prompt=args.no_prompt,
        write_config_only=args.write_config_only,
    )


if __name__ == "__main__":
    main()
