from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PolicyError(ValueError):
    """Raised when a job or worker violates the reciprocal local-only network rules."""


class JobStatus(str, Enum):
    QUEUED = "queued"
    ASSIGNED = "assigned"
    COMPLETED = "completed"
    FAILED = "failed"


class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"


@dataclass(frozen=True)
class ModelDefinition:
    tag: str
    family: str
    min_vram_gb: float
    input_credit_rate: float
    output_credit_rate: float
    quality_tier: str = "better"
    strength_score: float = 50.0
    runtime: str = "ollama"
    local_only: bool = True
    supports_public_pool: bool = True

    def estimate_credits(self, prompt_tokens: int, output_tokens: int) -> float:
        prompt_units = max(prompt_tokens, 1) / 1000.0
        output_units = max(output_tokens, 1) / 1000.0
        estimate = (prompt_units * self.input_credit_rate) + (
            output_units * self.output_credit_rate
        )
        return round(max(estimate, 0.25), 4)


@dataclass
class WorkerNode:
    worker_id: str
    owner_user_id: str
    gpu_name: str
    vram_gb: float
    installed_models: set[str]
    benchmark_tokens_per_second: dict[str, float]
    reliability_score: float = 1.0
    public_pool: bool = True
    online: bool = True
    max_concurrent_jobs: int = 1
    runtime: str = "ollama"
    allows_cloud_fallback: bool = False
    active_jobs: int = 0
    last_heartbeat_unix: float | None = None

    def supports_model(self, model: ModelDefinition) -> bool:
        return (
            self.online
            and self.public_pool
            and self.runtime == "ollama"
            and not self.allows_cloud_fallback
            and self.vram_gb >= model.min_vram_gb
            and model.tag in self.installed_models
            and self.benchmark_tokens_per_second.get(model.tag, 0.0) > 0.0
            and self.active_jobs < self.max_concurrent_jobs
        )


@dataclass(frozen=True)
class JobRequest:
    job_id: str
    requester_user_id: str
    model_tag: str
    prompt: str
    prompt_tokens: int
    max_output_tokens: int
    privacy_tier: str = "public"


@dataclass(frozen=True)
class JobAssignment:
    job_id: str
    worker_id: str
    model_tag: str
    reserved_credits: float
    prompt: str
    prompt_tokens: int
    max_output_tokens: int


@dataclass(frozen=True)
class JobResult:
    job_id: str
    worker_id: str
    success: bool
    output_tokens: int
    latency_seconds: float
    verified: bool
    output_text: str = ""
    error_message: str = ""


@dataclass
class JobRecord:
    request: JobRequest
    reserved_credits: float
    status: JobStatus = JobStatus.QUEUED
    assigned_worker_id: str | None = None
    resolved_model_tag: str | None = None
    actual_credits: float = 0.0
    result: JobResult | None = None


@dataclass(frozen=True)
class CreditHold:
    job_id: str
    user_id: str
    amount: float


@dataclass(frozen=True)
class CreditTransaction:
    user_id: str
    delta: float
    reason: str
    reference_id: str


@dataclass
class NetworkSnapshot:
    users: dict[str, float]
    queued_jobs: list[str]
    active_jobs: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutorResult:
    success: bool
    output_text: str
    output_tokens: int
    latency_seconds: float
    verified: bool = True
    error_message: str = ""
