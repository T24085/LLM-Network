from __future__ import annotations

import threading
from dataclasses import asdict
from pathlib import Path
from time import time
from typing import Callable
from uuid import uuid4

from .coordinator import OllamaNetworkCoordinator
from .executor import OllamaCommandExecutor
from .local_hardware import LocalHardwareDetector
from .catalog import QUALITY_SELECTORS
from .models import ExecutorResult, JobAssignment, JobResult, PolicyError, WorkerNode
from .ollama_local import LocalOllamaModelDetector
from .state_store import LocalStateStore


class NetworkService:
    """Thread-safe facade that exposes coordinator operations to the API server."""

    def __init__(
        self,
        coordinator: OllamaNetworkCoordinator | None = None,
        executor_factory: Callable[[str], object] | None = None,
        model_detector: object | None = None,
        hardware_detector: object | None = None,
        state_store: LocalStateStore | None = None,
    ) -> None:
        self.coordinator = coordinator or OllamaNetworkCoordinator()
        self._lock = threading.RLock()
        self._executor_factory = executor_factory or (lambda _worker_id: OllamaCommandExecutor())
        self._model_detector = model_detector or LocalOllamaModelDetector()
        self._hardware_detector = hardware_detector or LocalHardwareDetector()
        self._state_store = state_store or LocalStateStore(
            Path(__file__).resolve().parents[2] / ".runtime" / "private_state.json"
        )
        self._local_worker_loops: dict[str, dict[str, object]] = {}
        self._meta: dict[str, object] = {}
        self._load_state()

    def register_user(self, user_id: str, starting_credits: float = 0.0) -> dict[str, object]:
        with self._lock:
            self.coordinator.register_user(user_id=user_id, starting_credits=starting_credits)
            self._remember_user_locked(user_id)
            self._remember_local_operator_locked(user_id)
            self._persist_locked()
            return {
                "user_id": user_id,
                "balance": self.coordinator.ledger.balance_of(user_id),
            }

    def issue_user_identity(self, starting_credits: float = 0.0) -> dict[str, object]:
        with self._lock:
            user_id = self._generate_user_id_locked()
            self.coordinator.register_user(user_id=user_id, starting_credits=starting_credits)
            self._remember_user_locked(user_id)
            self._remember_local_operator_locked(user_id)
            self._persist_locked()
            return {
                "user_id": user_id,
                "balance": self.coordinator.ledger.balance_of(user_id),
                "issued": True,
            }

    def register_worker(self, payload: dict[str, object]) -> dict[str, object]:
        worker = WorkerNode(
            worker_id=str(payload["worker_id"]),
            owner_user_id=str(payload["owner_user_id"]),
            gpu_name=str(payload["gpu_name"]),
            vram_gb=float(payload["vram_gb"]),
            installed_models=set(payload["installed_models"]),
            benchmark_tokens_per_second={
                str(key): float(value)
                for key, value in dict(payload["benchmark_tokens_per_second"]).items()
            },
            reliability_score=float(payload.get("reliability_score", 1.0)),
            public_pool=bool(payload.get("public_pool", True)),
            online=bool(payload.get("online", True)),
            max_concurrent_jobs=int(payload.get("max_concurrent_jobs", 1)),
            runtime=str(payload.get("runtime", "ollama")),
            allows_cloud_fallback=bool(payload.get("allows_cloud_fallback", False)),
        )
        with self._lock:
            self.coordinator.register_worker(worker)
            self._persist_locked()
            return self.coordinator.worker_snapshot(worker.worker_id)

    def submit_job(self, payload: dict[str, object]) -> dict[str, object]:
        with self._lock:
            record = self.coordinator.submit_job(
                requester_user_id=str(payload["requester_user_id"]),
                model_tag=str(payload["model_tag"]),
                prompt=str(payload["prompt"]),
                max_output_tokens=int(payload["max_output_tokens"]),
                prompt_tokens=(
                    int(payload["prompt_tokens"])
                    if payload.get("prompt_tokens") is not None
                    else None
                ),
                privacy_tier=str(payload.get("privacy_tier", "public")),
            )
            self._remember_user_locked(str(payload["requester_user_id"]))
            self._persist_locked()
            return self.coordinator.job_snapshot(record.request.job_id)

    def claim_job_for_worker(self, worker_id: str) -> dict[str, object] | None:
        with self._lock:
            assignment = self.coordinator.claim_job_for_worker(worker_id)
            if assignment is None:
                return None
            self._persist_locked()
            return self._assignment_payload(assignment)

    def complete_job(self, payload: dict[str, object]) -> dict[str, object]:
        result = JobResult(
            job_id=str(payload["job_id"]),
            worker_id=str(payload["worker_id"]),
            success=bool(payload["success"]),
            output_tokens=int(payload["output_tokens"]),
            latency_seconds=float(payload["latency_seconds"]),
            verified=bool(payload.get("verified", True)),
            output_text=str(payload.get("output_text", "")),
            error_message=str(payload.get("error_message", "")),
        )
        with self._lock:
            record = self.coordinator.complete_job(result)
            self._persist_locked()
            return self.coordinator.job_snapshot(record.request.job_id)

    def get_job(self, job_id: str) -> dict[str, object]:
        with self._lock:
            return self.coordinator.job_snapshot(job_id)

    def get_user(self, user_id: str) -> dict[str, object]:
        with self._lock:
            if not self.coordinator.ledger.has_user(user_id):
                raise KeyError(user_id)
            self._remember_user_locked(user_id)
            self._persist_locked()
            return {
                "user_id": user_id,
                "balance": self.coordinator.ledger.balance_of(user_id),
            }

    def get_identity_context(self) -> dict[str, object]:
        with self._lock:
            balances = self.coordinator.ledger.export_state().get("balances", {})
            known_ids = sorted(str(user_id) for user_id in balances.keys())
            return {
                "last_active_user_id": self._meta.get("last_active_user_id"),
                "known_user_count": len(known_ids),
                "auto_selected_user_id": self._auto_selected_user_id_locked(known_ids),
            }

    def get_worker_context(self) -> dict[str, object]:
        with self._lock:
            balances = self.coordinator.ledger.export_state().get("balances", {})
            known_ids = sorted(str(user_id) for user_id in balances.keys())
            selected_user_id = self._auto_selected_user_id_locked(known_ids) or ""
            model_detection = self._model_detector.detect()
            hardware = self._hardware_detector.detect()
            available_vram_gb = hardware.primary_vram_gb if hardware.detected else 0.0
            approved_local_models = [
                model_tag
                for model_tag in model_detection.models
                if model_tag in self.coordinator.catalog.models
                and (
                    not available_vram_gb
                    or self.coordinator.catalog.models[model_tag].min_vram_gb <= available_vram_gb
                )
            ]
            return {
                "suggested_worker_id": selected_user_id,
                "suggested_owner_user_id": selected_user_id,
                "suggested_gpu_name": hardware.primary_gpu_name,
                "suggested_vram_gb": hardware.primary_vram_gb,
                "suggested_installed_models": approved_local_models,
                "suggested_benchmark_tokens_per_second": {
                    model_tag: self._default_tokens_per_second(model_tag)
                    for model_tag in approved_local_models
                },
                "hardware_detection": {
                    "detected": hardware.detected,
                    "primary_gpu_name": hardware.primary_gpu_name,
                    "primary_vram_gb": hardware.primary_vram_gb,
                    "gpus": [
                        {
                            "name": gpu.name,
                            "vram_gb": gpu.vram_gb,
                            "source": gpu.source,
                        }
                        for gpu in hardware.gpus
                    ],
                    "error": hardware.error,
                },
            }

    def list_models(self) -> dict[str, object]:
        with self._lock:
            detection = self._model_detector.detect()
            approved_tags = set(self.coordinator.catalog.models.keys())
            return {
                "models": [
                    {
                        "tag": model.tag,
                        "family": model.family,
                        "min_vram_gb": model.min_vram_gb,
                        "quality_tier": model.quality_tier,
                        "strength_score": model.strength_score,
                        "runtime": model.runtime,
                        "installed_locally": model.tag in detection.models,
                    }
                    for model in self.coordinator.catalog.models.values()
                ],
                "quality_selectors": list(QUALITY_SELECTORS),
                "local_detection": {
                    "ollama_available": detection.ollama_available,
                    "error": detection.error,
                    "detected_models": detection.models,
                    "approved_local_models": [
                        model_tag for model_tag in detection.models if model_tag in approved_tags
                    ],
                    "unapproved_local_models": [
                        model_tag for model_tag in detection.models if model_tag not in approved_tags
                    ],
                    "detection_scope": "api-server-host",
                },
            }

    def get_network(self) -> dict[str, object]:
        with self._lock:
            snapshot = self.coordinator.snapshot()
            return {
                "user_count": len(snapshot.users),
                "queued_jobs": snapshot.queued_jobs,
                "active_jobs": snapshot.active_jobs,
                "workers": {
                    worker_id: self.coordinator.worker_snapshot(worker_id)
                    for worker_id in self.coordinator.workers
                },
                "privacy": {
                    "balances_exposed": False,
                    "state_persisted_locally": self._state_store is not None,
                    "state_store_path": str(self._state_store.path) if self._state_store else "",
                },
                "local_workers": self._local_worker_statuses_locked(),
            }

    def run_worker_cycle(self, worker_id: str, executor: object | None = None) -> dict[str, object] | None:
        with self._lock:
            assignment = self.coordinator.claim_job_for_worker(worker_id)
            if assignment is None:
                return None
            selected_executor = executor or self._executor_factory(worker_id)
        try:
            execution: ExecutorResult = selected_executor.run(
                model_tag=assignment.model_tag,
                prompt=assignment.prompt,
                max_output_tokens=assignment.max_output_tokens,
            )
        except Exception as error:
            execution = ExecutorResult(
                success=False,
                output_text="",
                output_tokens=0,
                latency_seconds=0.0,
                verified=False,
                error_message=str(error),
            )
        result_payload = {
            "job_id": assignment.job_id,
            "worker_id": worker_id,
            "success": execution.success,
            "output_tokens": execution.output_tokens,
            "latency_seconds": execution.latency_seconds,
            "verified": execution.verified,
            "output_text": execution.output_text,
            "error_message": execution.error_message,
        }
        return self.complete_job(result_payload)

    def start_local_worker(self, payload: dict[str, object]) -> dict[str, object]:
        worker_id = str(payload["worker_id"])
        poll_interval_seconds = float(payload.get("poll_interval_seconds", 2.0))
        with self._lock:
            self._remember_local_operator_locked(str(payload["owner_user_id"]))
            worker_snapshot = self.register_worker(payload)
            existing = self._local_worker_loops.get(worker_id)
            if existing and existing["thread"].is_alive():
                existing["status"]["poll_interval_seconds"] = poll_interval_seconds
                return {
                    "worker": worker_snapshot,
                    "loop": dict(existing["status"]),
                }
            stop_event = threading.Event()
            status = {
                "worker_id": worker_id,
                "running": True,
                "poll_interval_seconds": poll_interval_seconds,
                "started_at_unix": time(),
                "last_job_id": None,
                "last_result_status": "idle",
                "last_error": "",
                "jobs_completed": 0,
            }
            thread = threading.Thread(
                target=self._local_worker_loop,
                args=(worker_id, poll_interval_seconds, stop_event),
                daemon=True,
            )
            self._local_worker_loops[worker_id] = {
                "thread": thread,
                "stop_event": stop_event,
                "status": status,
            }
            thread.start()
            return {
                "worker": worker_snapshot,
                "loop": dict(status),
            }

    def stop_local_worker(self, worker_id: str) -> dict[str, object]:
        with self._lock:
            session = self._local_worker_loops.get(worker_id)
            if session is None:
                if worker_id in self.coordinator.workers:
                    self.coordinator.update_worker(worker_id, online=False)
                    self._persist_locked()
                return {
                    "worker_id": worker_id,
                    "running": False,
                    "last_error": "",
                }
            session["stop_event"].set()
            session["status"]["running"] = False
            session["status"]["stopped_at_unix"] = time()
            if worker_id in self.coordinator.workers:
                self.coordinator.update_worker(worker_id, online=False)
                self._persist_locked()
            return dict(session["status"])

    @staticmethod
    def _assignment_payload(assignment: JobAssignment) -> dict[str, object]:
        return asdict(assignment)

    def _load_state(self) -> None:
        if self._state_store is None:
            return
        payload = self._state_store.load()
        if payload:
            if "coordinator" in payload:
                self.coordinator.import_state(dict(payload.get("coordinator", {})))
                self._meta = dict(payload.get("meta", {}))
            else:
                self.coordinator.import_state(payload)
                self._meta = {}

    def _persist_locked(self) -> None:
        if self._state_store is None:
            return
        self._state_store.save(
            {
                "coordinator": self.coordinator.export_state(),
                "meta": dict(self._meta),
            }
        )

    def _generate_user_id_locked(self) -> str:
        known_ids = set(self.coordinator.ledger.export_state().get("balances", {}).keys())
        while True:
            candidate = f"usr_{uuid4().hex[:12]}"
            if candidate not in known_ids:
                return candidate

    def _remember_user_locked(self, user_id: str) -> None:
        self._meta["last_active_user_id"] = user_id

    def _remember_local_operator_locked(self, user_id: str) -> None:
        self._meta["local_operator_user_id"] = user_id

    def _auto_selected_user_id_locked(self, known_ids: list[str]) -> str | None:
        local_operator = self._meta.get("local_operator_user_id")
        if isinstance(local_operator, str) and local_operator in known_ids:
            return local_operator
        last_active = self._meta.get("last_active_user_id")
        if isinstance(last_active, str) and last_active in known_ids:
            return last_active
        transactions = list(self.coordinator.ledger.export_state().get("transactions", []))
        for item in reversed(transactions):
            user_id = str(item.get("user_id", ""))
            if user_id.startswith("usr_") and user_id in known_ids:
                return user_id
        if len(known_ids) == 1:
            return known_ids[0]
        return None

    def _local_worker_statuses_locked(self) -> dict[str, dict[str, object]]:
        statuses: dict[str, dict[str, object]] = {}
        for worker_id, session in self._local_worker_loops.items():
            statuses[worker_id] = dict(session["status"])
            statuses[worker_id]["thread_alive"] = session["thread"].is_alive()
        return statuses

    def _local_worker_loop(
        self,
        worker_id: str,
        poll_interval_seconds: float,
        stop_event: threading.Event,
    ) -> None:
        executor = self._executor_factory(worker_id)
        while not stop_event.is_set():
            try:
                result = self.run_worker_cycle(worker_id, executor=executor)
                with self._lock:
                    session = self._local_worker_loops.get(worker_id)
                    if session is not None:
                        session["status"]["running"] = True
                        session["status"]["last_error"] = ""
                        session["status"]["last_polled_unix"] = time()
                        if result is None:
                            session["status"]["last_result_status"] = "idle"
                        else:
                            session["status"]["last_job_id"] = result["job_id"]
                            session["status"]["last_result_status"] = result["status"]
                            if result["status"] == "completed":
                                session["status"]["jobs_completed"] += 1
            except Exception as error:
                with self._lock:
                    session = self._local_worker_loops.get(worker_id)
                    if session is not None:
                        session["status"]["running"] = True
                        session["status"]["last_error"] = str(error)
                        session["status"]["last_result_status"] = "error"
                        session["status"]["last_polled_unix"] = time()
            stop_event.wait(poll_interval_seconds)

    @staticmethod
    def _default_tokens_per_second(model_tag: str) -> float:
        numeric_chunks = [
            int(chunk.rstrip("b"))
            for chunk in model_tag.replace(":", "-").split("-")
            if chunk.endswith("b") and chunk[:-1].isdigit()
        ]
        if not numeric_chunks:
            return 24.0
        size = numeric_chunks[0]
        if size <= 4:
            return 72.0
        if size <= 9:
            return 48.0
        if size <= 20:
            return 24.0
        return 12.0


def handle_policy_error(error: PolicyError) -> tuple[int, dict[str, str]]:
    return 400, {"error": str(error)}
