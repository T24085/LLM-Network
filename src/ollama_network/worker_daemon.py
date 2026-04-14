from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union
from urllib import error, request

from .constants import DEFAULT_PUBLIC_SERVER_URL
from .executor import OllamaCommandExecutor
from .local_hardware import LocalHardwareDetector
from .models import ExecutorResult
from .ollama_local import LocalOllamaModelDetector


class WorkerBootstrapError(RuntimeError):
    pass


@dataclass(frozen=True)
class WorkerConfig:
    server_url: str = DEFAULT_PUBLIC_SERVER_URL
    worker_id: str = ""
    owner_user_id: str = ""
    worker_name: str = ""
    gpu_name: str = ""
    vram_gb: float = 0.0
    installed_models: tuple[str, ...] = ()
    benchmark_tokens_per_second: dict[str, float] = field(default_factory=dict)
    system_ram_gb: float = 0.0
    machine_name: str = ""
    platform: str = ""
    poll_interval_seconds: float = 2.0
    heartbeat_interval_seconds: float = 30.0
    max_concurrent_jobs: int = 1
    worker_token: str = ""
    firebase_id_token: str = ""
    auto_detect_models: bool = True
    auto_detect_hardware: bool = True
    config_source: str = ""


class WorkerDaemon:
    def __init__(
        self,
        config: WorkerConfig,
        executor: Optional[Union[OllamaCommandExecutor, object]] = None,
    ) -> None:
        self.config = config
        self.executor = executor or OllamaCommandExecutor()
        self._local_runtime_path = Path.cwd() / ".runtime" / "worker.local.json"

    def register(self) -> dict[str, object]:
        return self._post("/worker/register", self._worker_payload())

    def heartbeat(self) -> dict[str, object]:
        return self._post("/worker/heartbeat", self._worker_payload())

    def run_once(self) -> Optional[dict[str, object]]:
        claimed = self._post(f"/workers/{self.config.worker_id}/claim", {})
        assignment = claimed.get("assignment")
        if assignment is None:
            return None
        try:
            result: ExecutorResult = self.executor.run(
                model_tag=str(assignment["model_tag"]),
                prompt=str(assignment["prompt"]),
                max_output_tokens=int(assignment["max_output_tokens"]),
            )
        except Exception as error:  # pragma: no cover - local executor failure
            result = ExecutorResult(
                success=False,
                output_text="",
                output_tokens=0,
                latency_seconds=0.0,
                verified=False,
                error_message=str(error),
            )
        payload = {
            "job_id": assignment["job_id"],
            "worker_id": self.config.worker_id,
            "success": result.success,
            "output_tokens": result.output_tokens,
            "latency_seconds": result.latency_seconds,
            "verified": result.verified,
            "prompt_tokens_used": result.prompt_tokens_used,
            "output_text": result.output_text,
            "error_message": result.error_message,
        }
        return self._post("/jobs/complete", payload)

    def serve_forever(self) -> None:
        self._register_with_retries()
        last_heartbeat = 0.0
        while True:
            now = time.time()
            try:
                if now - last_heartbeat >= max(self.config.heartbeat_interval_seconds, 1.0):
                    heartbeat = self.heartbeat()
                    self._save_local_config(heartbeat)
                    last_heartbeat = now
                result = self.run_once()
                if result is not None:
                    self._save_local_config(result)
                time.sleep(max(self.config.poll_interval_seconds, 0.5))
            except WorkerBootstrapError:
                raise
            except RuntimeError as error:
                print(f"Worker connection issue: {error}", file=sys.stderr)
                time.sleep(min(15.0, max(self.config.poll_interval_seconds, 2.0)))

    def _register_with_retries(self) -> dict[str, object]:
        while True:
            try:
                result = self.register()
                self._save_local_config(result)
                return result
            except WorkerBootstrapError:
                raise
            except RuntimeError as error:
                print(f"Worker registration failed: {error}", file=sys.stderr)
                time.sleep(5.0)

    def _worker_payload(self) -> dict[str, object]:
        return {
            "worker_id": self.config.worker_id,
            "owner_user_id": self.config.owner_user_id,
            "worker_name": self.config.worker_name,
            "machine_name": self.config.machine_name,
            "platform": self.config.platform,
            "server_url": self.config.server_url,
            "gpu_name": self.config.gpu_name,
            "vram_gb": self.config.vram_gb,
            "system_ram_gb": self.config.system_ram_gb,
            "installed_models": list(self.config.installed_models),
            "benchmark_tokens_per_second": self.config.benchmark_tokens_per_second,
            "max_concurrent_jobs": self.config.max_concurrent_jobs,
            "runtime": "ollama",
            "allows_cloud_fallback": False,
            "worker_token": self.config.worker_token,
        }

    def _save_local_config(self, server_payload: Optional[dict[str, object]] = None) -> None:
        payload = {
            "server_url": self.config.server_url,
            "worker_id": self.config.worker_id,
            "owner_user_id": self.config.owner_user_id,
            "worker_name": self.config.worker_name,
            "worker_token": self.config.worker_token,
            "gpu_name": self.config.gpu_name,
            "vram_gb": self.config.vram_gb,
            "system_ram_gb": self.config.system_ram_gb,
            "installed_models": list(self.config.installed_models),
            "benchmark_tokens_per_second": self.config.benchmark_tokens_per_second,
            "machine_name": self.config.machine_name,
            "platform": self.config.platform,
            "poll_interval_seconds": self.config.poll_interval_seconds,
            "heartbeat_interval_seconds": self.config.heartbeat_interval_seconds,
            "max_concurrent_jobs": self.config.max_concurrent_jobs,
            "auto_detect_models": self.config.auto_detect_models,
            "auto_detect_hardware": self.config.auto_detect_hardware,
        }
        if server_payload:
            payload["registered_at_unix"] = float(
                server_payload.get("enrollment_registered_at_unix")
                or server_payload.get("registered_at_unix")
                or server_payload.get("last_heartbeat_unix")
                or 0.0
            )
            payload["last_seen_at_unix"] = float(server_payload.get("last_heartbeat_unix") or 0.0)
            payload["server_worker_status"] = str(
                (server_payload.get("enrollment") or {}).get("status", "")
                if isinstance(server_payload.get("enrollment"), dict)
                else ""
            )
        self._local_runtime_path.parent.mkdir(parents=True, exist_ok=True)
        self._local_runtime_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _post(self, path: str, payload: dict[str, object]) -> dict[str, object]:
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.config.worker_token:
            headers["X-Worker-Token"] = self.config.worker_token
        if self.config.firebase_id_token:
            headers["Authorization"] = f"Bearer {self.config.firebase_id_token}"
        req = request.Request(
            url=f"{self.config.server_url.rstrip('/')}{path}",
            data=body,
            headers=headers,
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=30) as response:
                data = response.read().decode("utf-8")
                return json.loads(data) if data else {}
        except error.HTTPError as http_error:
            detail = http_error.read().decode("utf-8")
            message = f"API request failed: {http_error.code} {detail}"
            if http_error.code in {400, 401, 403}:
                raise WorkerBootstrapError(message) from http_error
            raise RuntimeError(message) from http_error
        except error.URLError as url_error:
            raise RuntimeError(str(url_error)) from url_error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an Ollama Network worker daemon.")
    parser.add_argument("--config", default=os.environ.get("OLLAMA_NETWORK_WORKER_CONFIG", ""), help="Path to llm-network-worker.json or worker.local.json.")
    parser.add_argument("--server-url", default=os.environ.get("OLLAMA_NETWORK_SERVER_URL", ""), help="Coordinator API URL.")
    parser.add_argument("--worker-id", default=os.environ.get("OLLAMA_NETWORK_WORKER_ID", ""), help="Stable worker identifier.")
    parser.add_argument("--owner-user-id", default=os.environ.get("OLLAMA_NETWORK_OWNER_USER_ID", ""), help="User id that owns this worker.")
    parser.add_argument("--worker-name", default=os.environ.get("OLLAMA_NETWORK_WORKER_NAME", ""), help="Display name for the worker.")
    parser.add_argument("--machine-name", default=os.environ.get("OLLAMA_NETWORK_MACHINE_NAME", ""), help="Machine hostname override.")
    parser.add_argument("--platform", default=os.environ.get("OLLAMA_NETWORK_PLATFORM", ""), help="Platform label override.")
    parser.add_argument("--gpu-name", default="", help="GPU label advertised to the network. Defaults to local hardware detection.")
    parser.add_argument("--vram-gb", type=float, default=0.0, help="Available GPU VRAM. Defaults to local hardware detection.")
    parser.add_argument("--system-ram-gb", type=float, default=0.0, help="Available host RAM. Defaults to local hardware detection.")
    parser.add_argument("--model", action="append", dest="models", default=[], help="Approved Ollama model tag. Repeatable.")
    parser.add_argument("--tps", action="append", dest="throughput_entries", default=[], help="Throughput entry in MODEL=TPS format. Repeatable.")
    parser.add_argument("--poll-interval", type=float, default=2.0, help="Poll interval in seconds.")
    parser.add_argument("--heartbeat-interval", type=float, default=30.0, help="Heartbeat interval in seconds.")
    parser.add_argument("--max-concurrent-jobs", type=int, default=1, help="Maximum concurrent jobs.")
    parser.add_argument("--worker-token", default=os.environ.get("OLLAMA_NETWORK_WORKER_TOKEN", ""), help="Long-lived worker token issued by the coordinator.")
    parser.add_argument("--firebase-id-token", default=os.environ.get("OLLAMA_NETWORK_FIREBASE_ID_TOKEN", ""), help="Optional Firebase ID token for protected servers.")
    parser.add_argument("--debug", action="store_true", help="Print tracebacks instead of friendly startup errors.")
    return parser


def resolve_worker_config(args: argparse.Namespace) -> WorkerConfig:
    file_config = load_worker_config_file(args.config)
    if not args.server_url and file_config.get("server_url"):
        args.server_url = str(file_config.get("server_url", ""))
    if not args.worker_id and file_config.get("worker_id"):
        args.worker_id = str(file_config.get("worker_id", ""))
    if not args.owner_user_id and file_config.get("owner_user_id"):
        args.owner_user_id = str(file_config.get("owner_user_id", ""))
    if not args.worker_name and file_config.get("worker_name"):
        args.worker_name = str(file_config.get("worker_name", ""))
    if not args.machine_name and file_config.get("machine_name"):
        args.machine_name = str(file_config.get("machine_name", ""))
    if not args.platform and file_config.get("platform"):
        args.platform = str(file_config.get("platform", ""))
    if not args.gpu_name and file_config.get("gpu_name"):
        args.gpu_name = str(file_config.get("gpu_name", ""))
    if not args.vram_gb and file_config.get("vram_gb") is not None:
        args.vram_gb = float(file_config.get("vram_gb", 0.0))
    if not args.system_ram_gb and file_config.get("system_ram_gb") is not None:
        args.system_ram_gb = float(file_config.get("system_ram_gb", 0.0))
    if not args.worker_token and file_config.get("worker_token"):
        args.worker_token = str(file_config.get("worker_token", ""))
    if file_config.get("poll_interval_seconds") is not None and args.poll_interval == 2.0:
        args.poll_interval = float(file_config.get("poll_interval_seconds", 2.0))
    if file_config.get("heartbeat_interval_seconds") is not None and args.heartbeat_interval == 30.0:
        args.heartbeat_interval = float(file_config.get("heartbeat_interval_seconds", 30.0))
    if file_config.get("max_concurrent_jobs") is not None and args.max_concurrent_jobs == 1:
        args.max_concurrent_jobs = int(file_config.get("max_concurrent_jobs", 1))

    hardware_detector = LocalHardwareDetector()
    model_detector = LocalOllamaModelDetector()
    hardware = hardware_detector.detect()
    model_detection = model_detector.detect()
    auto_detect_models = bool(file_config.get("auto_detect_models", True))
    auto_detect_hardware = bool(file_config.get("auto_detect_hardware", True))

    models = list(args.models or file_config.get("installed_models", []) or [])
    if auto_detect_models:
        if not model_detection.ollama_available:
            raise WorkerBootstrapError(
                "Ollama was not detected. Install Ollama, then place llm-network-worker.json next to start_worker_daemon.bat and run it again."
            )
        if not models and model_detection.models:
            models = list(model_detection.models)
    if auto_detect_models and not models:
        raise WorkerBootstrapError(
            "No Ollama models were detected. Install at least one local model, then rerun the worker launcher."
        )

    gpu_name = str(args.gpu_name or file_config.get("gpu_name", "") or (hardware.primary_gpu_name if auto_detect_hardware and hardware.detected else "") or "Unknown GPU").strip()
    vram_gb = float(args.vram_gb or file_config.get("vram_gb", 0.0) or (hardware.primary_vram_gb if auto_detect_hardware and hardware.detected else 0.0) or 0.0)
    system_ram_gb = float(args.system_ram_gb or file_config.get("system_ram_gb", 0.0) or (hardware.system_ram_gb if auto_detect_hardware and hardware.detected else 0.0) or 0.0)
    machine_name = str(args.machine_name or file_config.get("machine_name", "") or socket.gethostname()).strip() or socket.gethostname()
    platform_name = str(args.platform or file_config.get("platform", "") or sys.platform).strip() or sys.platform
    worker_name = str(args.worker_name or file_config.get("worker_name", "") or machine_name or args.worker_id or "").strip()
    server_url = str(args.server_url or file_config.get("server_url", "") or DEFAULT_PUBLIC_SERVER_URL).strip() or DEFAULT_PUBLIC_SERVER_URL
    worker_id = str(args.worker_id or file_config.get("worker_id", "") or "").strip()
    owner_user_id = str(args.owner_user_id or file_config.get("owner_user_id", "") or "").strip()
    worker_token = str(args.worker_token or file_config.get("worker_token", "") or "").strip()

    if not worker_id or not owner_user_id or not worker_token:
        raise WorkerBootstrapError(
            "Worker config is missing required fields. Download llm-network-worker.json from the dashboard and place it next to start_worker_daemon.bat."
        )

    if not worker_name:
        worker_name = machine_name or worker_id

    benchmark_tokens_per_second = dict(file_config.get("benchmark_tokens_per_second", {}) or {})
    benchmark_tokens_per_second.update(parse_throughput(args.throughput_entries, models))
    for model_tag in models:
        benchmark_tokens_per_second.setdefault(model_tag, 1.0)

    return WorkerConfig(
        server_url=server_url,
        worker_id=worker_id,
        owner_user_id=owner_user_id,
        worker_name=worker_name,
        gpu_name=gpu_name,
        vram_gb=vram_gb,
        installed_models=tuple(models),
        benchmark_tokens_per_second=benchmark_tokens_per_second,
        system_ram_gb=system_ram_gb,
        machine_name=machine_name,
        platform=platform_name,
        poll_interval_seconds=float(args.poll_interval),
        heartbeat_interval_seconds=float(args.heartbeat_interval),
        max_concurrent_jobs=int(args.max_concurrent_jobs),
        worker_token=worker_token,
        firebase_id_token=str(args.firebase_id_token or file_config.get("firebase_id_token", "") or ""),
        auto_detect_models=auto_detect_models,
        auto_detect_hardware=auto_detect_hardware,
        config_source=str(args.config or discover_worker_config_path() or ""),
    )


def load_worker_config_file(config_path: str) -> dict[str, object]:
    resolved = discover_worker_config_path(config_path)
    if resolved is None:
        if config_path:
            raise WorkerBootstrapError(f"Worker config file was not found: {config_path}")
        return {}
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("config"), dict):
        payload = dict(payload["config"])
    if not isinstance(payload, dict):
        raise WorkerBootstrapError(f"Worker config at {resolved} must be a JSON object.")
    return payload


def discover_worker_config_path(config_path: str = "") -> Optional[Path]:
    candidates = []
    if config_path:
        explicit = Path(config_path).expanduser()
        return explicit if explicit.is_file() else None
    candidates.extend(
        [
            Path.cwd() / ".runtime" / "worker.local.json",
            Path.cwd() / "llm-network-worker.json",
        ]
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def parse_throughput(entries: list[str], models: list[str]) -> dict[str, float]:
    throughput: dict[str, float] = {}
    for entry in entries:
        if "=" not in entry:
            raise WorkerBootstrapError(f"Invalid throughput entry '{entry}'. Expected MODEL=TPS.")
        model_tag, value = entry.split("=", maxsplit=1)
        throughput[model_tag.strip()] = float(value)
    for model_tag in models:
        throughput.setdefault(model_tag, 1.0)
    return throughput


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        config = resolve_worker_config(args)
        daemon = WorkerDaemon(config=config)
        print(
            f"Worker {config.worker_id} serving {', '.join(config.installed_models) or 'no models'} via {config.server_url}"
        )
        daemon.serve_forever()
    except WorkerBootstrapError as error:
        print(str(error), file=sys.stderr)
        if args.debug:
            traceback.print_exc()
        raise SystemExit(1) from error
    except KeyboardInterrupt:
        raise SystemExit(0)
    except Exception as error:
        if args.debug:
            traceback.print_exc()
        else:
            print(str(error), file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
