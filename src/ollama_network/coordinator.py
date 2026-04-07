from __future__ import annotations

from collections import deque
from dataclasses import asdict
from time import time
from uuid import uuid4

from .catalog import ApprovedModelCatalog
from .ledger import CreditLedger
from .models import (
    JobAssignment,
    JobRecord,
    JobRequest,
    JobResult,
    JobStatus,
    NetworkSnapshot,
    PolicyError,
    WorkerNode,
)


class OllamaNetworkCoordinator:
    """In-memory coordinator for a reciprocal local-only Ollama worker pool."""

    def __init__(
        self,
        catalog: ApprovedModelCatalog | None = None,
        ledger: CreditLedger | None = None,
    ) -> None:
        self.catalog = catalog or ApprovedModelCatalog.default()
        self.ledger = ledger or CreditLedger()
        self.workers: dict[str, WorkerNode] = {}
        self.jobs: dict[str, JobRecord] = {}
        self._queued_job_ids: deque[str] = deque()

    def register_user(self, user_id: str, starting_credits: float = 0.0) -> None:
        self.ledger.register_user(user_id=user_id, starting_credits=starting_credits)

    def register_worker(self, worker: WorkerNode) -> None:
        if not worker.worker_id.strip():
            raise PolicyError("Worker ID is required.")
        if not worker.owner_user_id.strip():
            raise PolicyError("Worker owner user ID is required.")
        if not worker.gpu_name.strip():
            raise PolicyError("GPU name is required.")
        if not worker.installed_models:
            raise PolicyError("At least one installed Ollama model is required.")
        if worker.runtime != "ollama" or worker.allows_cloud_fallback:
            raise PolicyError("Workers must run Ollama locally with cloud fallback disabled.")
        for model_tag in worker.installed_models:
            self.catalog.require_local_model(model_tag)
        self.register_user(worker.owner_user_id)
        worker.last_heartbeat_unix = time()
        self.workers[worker.worker_id] = worker

    def update_worker(self, worker_id: str, online: bool = True) -> WorkerNode:
        worker = self.workers[worker_id]
        worker.online = online
        worker.last_heartbeat_unix = time()
        return worker

    def submit_job(
        self,
        requester_user_id: str,
        model_tag: str,
        prompt: str,
        max_output_tokens: int,
        prompt_tokens: int | None = None,
        privacy_tier: str = "public",
    ) -> JobRecord:
        if privacy_tier != "public":
            raise PolicyError(
                "This volunteer network only accepts public jobs until secure attestation is added."
            )
        selector = self.catalog.normalize_selector(model_tag)
        self.register_user(requester_user_id)
        estimated_prompt_tokens = prompt_tokens or self._estimate_prompt_tokens(prompt)
        reserved_credits = self.catalog.estimate_reservation(
            selector=selector,
            prompt_tokens=estimated_prompt_tokens,
            max_output_tokens=max_output_tokens,
        )
        job_id = f"job-{uuid4().hex[:10]}"
        request = JobRequest(
            job_id=job_id,
            requester_user_id=requester_user_id,
            model_tag=selector,
            prompt=prompt,
            prompt_tokens=estimated_prompt_tokens,
            max_output_tokens=max_output_tokens,
            privacy_tier=privacy_tier,
        )
        self.ledger.reserve(user_id=requester_user_id, job_id=job_id, amount=reserved_credits)
        record = JobRecord(request=request, reserved_credits=reserved_credits)
        self.jobs[job_id] = record
        self._queued_job_ids.append(job_id)
        return record

    def assign_next_job(self) -> JobAssignment | None:
        for _ in range(len(self._queued_job_ids)):
            job_id = self._queued_job_ids.popleft()
            record = self.jobs[job_id]
            if record.status is not JobStatus.QUEUED:
                continue
            worker = self._select_worker(record)
            if worker is None:
                self._queued_job_ids.append(job_id)
                continue
            resolved_model = self._resolve_model_for_worker(worker, record.request.model_tag)
            if resolved_model is None:
                self._queued_job_ids.append(job_id)
                continue
            record.status = JobStatus.ASSIGNED
            record.assigned_worker_id = worker.worker_id
            record.resolved_model_tag = resolved_model.tag
            worker.active_jobs += 1
            return JobAssignment(
                job_id=job_id,
                worker_id=worker.worker_id,
                model_tag=resolved_model.tag,
                reserved_credits=record.reserved_credits,
                prompt=record.request.prompt,
                prompt_tokens=record.request.prompt_tokens,
                max_output_tokens=record.request.max_output_tokens,
            )
        return None

    def claim_job_for_worker(self, worker_id: str) -> JobAssignment | None:
        worker = self.update_worker(worker_id=worker_id, online=True)
        for _ in range(len(self._queued_job_ids)):
            job_id = self._queued_job_ids.popleft()
            record = self.jobs[job_id]
            if record.status is not JobStatus.QUEUED:
                continue
            resolved_model = self._resolve_model_for_worker(worker, record.request.model_tag)
            if (
                worker.owner_user_id == record.request.requester_user_id
                or resolved_model is None
                or not worker.supports_model(resolved_model)
            ):
                self._queued_job_ids.append(job_id)
                continue
            record.status = JobStatus.ASSIGNED
            record.assigned_worker_id = worker.worker_id
            record.resolved_model_tag = resolved_model.tag
            worker.active_jobs += 1
            return JobAssignment(
                job_id=job_id,
                worker_id=worker.worker_id,
                model_tag=resolved_model.tag,
                reserved_credits=record.reserved_credits,
                prompt=record.request.prompt,
                prompt_tokens=record.request.prompt_tokens,
                max_output_tokens=record.request.max_output_tokens,
            )
        return None

    def complete_job(self, result: JobResult) -> JobRecord:
        record = self.jobs[result.job_id]
        if record.assigned_worker_id != result.worker_id:
            raise PolicyError("Job results must come from the assigned worker.")
        worker = self.workers[result.worker_id]
        worker.last_heartbeat_unix = time()
        worker.active_jobs = max(worker.active_jobs - 1, 0)
        record.result = result
        if not result.success or not result.verified:
            self.ledger.release(
                job_id=result.job_id,
                reason="job failed or could not be verified",
            )
            record.status = JobStatus.FAILED
            return record
        if worker.owner_user_id == record.request.requester_user_id:
            self.ledger.release(
                job_id=result.job_id,
                reason="self-served work does not earn reciprocal credits",
            )
            record.status = JobStatus.COMPLETED
            return record
        actual_credits = min(
            record.reserved_credits,
            self.catalog.actual_cost(
                selector=record.request.model_tag,
                resolved_model_tag=record.resolved_model_tag or record.request.model_tag,
                prompt_tokens=record.request.prompt_tokens,
                output_tokens=result.output_tokens,
            ),
        )
        transferred, _ = self.ledger.settle(
            job_id=result.job_id,
            worker_user_id=worker.owner_user_id,
            amount_to_worker=actual_credits,
        )
        record.actual_credits = transferred
        record.status = JobStatus.COMPLETED
        return record

    def snapshot(self) -> NetworkSnapshot:
        return NetworkSnapshot(
            users={user_id: self.ledger.balance_of(user_id) for user_id in self._known_users()},
            queued_jobs=list(self._queued_job_ids),
            active_jobs={
                worker_id: worker.active_jobs for worker_id, worker in self.workers.items()
            },
        )

    def worker_snapshot(self, worker_id: str) -> dict[str, object]:
        worker = self.workers[worker_id]
        payload = asdict(worker)
        payload["installed_models"] = sorted(worker.installed_models)
        return payload

    def job_snapshot(self, job_id: str) -> dict[str, object]:
        record = self.jobs[job_id]
        payload = {
            "job_id": record.request.job_id,
            "requester_user_id": record.request.requester_user_id,
            "model_tag": record.request.model_tag,
            "resolved_model_tag": record.resolved_model_tag,
            "prompt": record.request.prompt,
            "prompt_tokens": record.request.prompt_tokens,
            "max_output_tokens": record.request.max_output_tokens,
            "privacy_tier": record.request.privacy_tier,
            "reserved_credits": record.reserved_credits,
            "status": record.status.value,
            "assigned_worker_id": record.assigned_worker_id,
            "actual_credits": record.actual_credits,
            "result": asdict(record.result) if record.result else None,
        }
        return payload

    def _known_users(self) -> set[str]:
        known = set(self.ledger.export_state().get("balances", {}).keys())
        known.update(worker.owner_user_id for worker in self.workers.values())
        known.update(record.request.requester_user_id for record in self.jobs.values())
        return known

    @staticmethod
    def _estimate_prompt_tokens(prompt: str) -> int:
        word_count = len([token for token in prompt.split() if token.strip()])
        return max(8, word_count * 2)

    def _select_worker(self, record: JobRecord) -> WorkerNode | None:
        candidates = [
            worker
            for worker in self.workers.values()
            if worker.owner_user_id != record.request.requester_user_id
        ]
        scored_candidates: list[tuple[WorkerNode, str]] = []
        for worker in candidates:
            resolved_model = self._resolve_model_for_worker(worker, record.request.model_tag)
            if resolved_model is None or not worker.supports_model(resolved_model):
                continue
            scored_candidates.append((worker, resolved_model.tag))
        if not scored_candidates:
            return None
        return max(
            scored_candidates,
            key=lambda item: self._worker_score(item[0], item[1]),
        )[0]

    @staticmethod
    def _worker_score(worker: WorkerNode, model_tag: str) -> float:
        return (
            worker.benchmark_tokens_per_second.get(model_tag, 0.0)
            * max(worker.reliability_score, 0.1)
        )

    def _resolve_model_for_worker(self, worker: WorkerNode, selector: str):
        supported_models = {
            model_tag
            for model_tag in worker.installed_models
            if model_tag in self.catalog.models
            and worker.supports_model(self.catalog.models[model_tag])
        }
        return self.catalog.resolve_selector_for_models(selector, supported_models)

    def export_state(self) -> dict[str, object]:
        return {
            "workers": {
                worker_id: self.worker_snapshot(worker_id)
                for worker_id in self.workers
            },
            "jobs": {
                job_id: self.job_snapshot(job_id)
                for job_id in self.jobs
            },
            "queued_job_ids": list(self._queued_job_ids),
            "ledger": self.ledger.export_state(),
        }

    def import_state(self, payload: dict[str, object]) -> None:
        self.workers = {}
        for worker_id, worker_payload in dict(payload.get("workers", {})).items():
            candidate = WorkerNode(
                worker_id=str(worker_payload["worker_id"]),
                owner_user_id=str(worker_payload["owner_user_id"]),
                gpu_name=str(worker_payload["gpu_name"]),
                vram_gb=float(worker_payload["vram_gb"]),
                installed_models=set(worker_payload.get("installed_models", [])),
                benchmark_tokens_per_second={
                    str(key): float(value)
                    for key, value in dict(
                        worker_payload.get("benchmark_tokens_per_second", {})
                    ).items()
                },
                reliability_score=float(worker_payload.get("reliability_score", 1.0)),
                public_pool=bool(worker_payload.get("public_pool", True)),
                online=bool(worker_payload.get("online", True)),
                max_concurrent_jobs=int(worker_payload.get("max_concurrent_jobs", 1)),
                runtime=str(worker_payload.get("runtime", "ollama")),
                allows_cloud_fallback=bool(worker_payload.get("allows_cloud_fallback", False)),
                active_jobs=int(worker_payload.get("active_jobs", 0)),
                last_heartbeat_unix=(
                    float(worker_payload["last_heartbeat_unix"])
                    if worker_payload.get("last_heartbeat_unix") is not None
                    else None
                ),
            )
            try:
                self.register_worker(candidate)
            except PolicyError:
                continue

        self.jobs = {}
        for job_id, job_payload in dict(payload.get("jobs", {})).items():
            result_payload = job_payload.get("result")
            result = (
                JobResult(
                    job_id=str(result_payload["job_id"]),
                    worker_id=str(result_payload["worker_id"]),
                    success=bool(result_payload["success"]),
                    output_tokens=int(result_payload["output_tokens"]),
                    latency_seconds=float(result_payload["latency_seconds"]),
                    verified=bool(result_payload["verified"]),
                    output_text=str(result_payload.get("output_text", "")),
                    error_message=str(result_payload.get("error_message", "")),
                )
                if result_payload
                else None
            )
            self.jobs[str(job_id)] = JobRecord(
                request=JobRequest(
                    job_id=str(job_payload["job_id"]),
                    requester_user_id=str(job_payload["requester_user_id"]),
                    model_tag=str(job_payload["model_tag"]),
                    prompt=str(job_payload["prompt"]),
                    prompt_tokens=int(job_payload["prompt_tokens"]),
                    max_output_tokens=int(job_payload["max_output_tokens"]),
                    privacy_tier=str(job_payload.get("privacy_tier", "public")),
                ),
                reserved_credits=float(job_payload["reserved_credits"]),
                status=JobStatus(str(job_payload["status"])),
                assigned_worker_id=(
                    str(job_payload["assigned_worker_id"])
                    if job_payload.get("assigned_worker_id") is not None
                    else None
                ),
                resolved_model_tag=(
                    str(job_payload["resolved_model_tag"])
                    if job_payload.get("resolved_model_tag") is not None
                    else None
                ),
                actual_credits=float(job_payload.get("actual_credits", 0.0)),
                result=result,
            )

        self._queued_job_ids = deque(str(job_id) for job_id in payload.get("queued_job_ids", []))
        self.ledger.import_state(dict(payload.get("ledger", {})))
