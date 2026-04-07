from __future__ import annotations

from dataclasses import dataclass

from .models import ModelDefinition, PolicyError

QUALITY_SELECTORS = ("auto", "good", "better", "best")
QUALITY_MULTIPLIERS = {
    "auto": 1.0,
    "good": 1.0,
    "better": 1.1,
    "best": 1.2,
}

DEFAULT_OLLAMA_MODELS: tuple[ModelDefinition, ...] = (
    ModelDefinition(
        tag="qwen3:4b",
        family="qwen",
        min_vram_gb=4.0,
        input_credit_rate=0.28,
        output_credit_rate=0.62,
        quality_tier="good",
        strength_score=42.0,
    ),
    ModelDefinition(
        tag="glm4:9b",
        family="glm",
        min_vram_gb=8.0,
        input_credit_rate=0.42,
        output_credit_rate=0.88,
        quality_tier="better",
        strength_score=74.0,
    ),
    ModelDefinition(
        tag="deepseek-r1:8b",
        family="deepseek",
        min_vram_gb=8.0,
        input_credit_rate=0.46,
        output_credit_rate=0.96,
        quality_tier="better",
        strength_score=76.0,
    ),
    ModelDefinition(
        tag="gpt-oss:20b",
        family="gpt-oss",
        min_vram_gb=16.0,
        input_credit_rate=0.78,
        output_credit_rate=1.38,
        quality_tier="best",
        strength_score=96.0,
    ),
    ModelDefinition(
        tag="llama3.1:8b",
        family="llama",
        min_vram_gb=8.0,
        input_credit_rate=0.5,
        output_credit_rate=1.0,
        quality_tier="better",
        strength_score=71.0,
    ),
    ModelDefinition(
        tag="mistral:7b",
        family="mistral",
        min_vram_gb=8.0,
        input_credit_rate=0.45,
        output_credit_rate=0.95,
        quality_tier="better",
        strength_score=64.0,
    ),
    ModelDefinition(
        tag="qwen2.5:7b",
        family="qwen",
        min_vram_gb=8.0,
        input_credit_rate=0.4,
        output_credit_rate=0.9,
        quality_tier="better",
        strength_score=66.0,
    ),
    ModelDefinition(
        tag="phi4:14b",
        family="phi",
        min_vram_gb=16.0,
        input_credit_rate=0.7,
        output_credit_rate=1.25,
        quality_tier="best",
        strength_score=88.0,
    ),
)


@dataclass
class ApprovedModelCatalog:
    models: dict[str, ModelDefinition]

    @classmethod
    def default(cls) -> "ApprovedModelCatalog":
        return cls(models={model.tag: model for model in DEFAULT_OLLAMA_MODELS})

    def require_local_model(self, model_tag: str) -> ModelDefinition:
        model = self.models.get(model_tag)
        if model is None:
            raise PolicyError(
                f"Model '{model_tag}' is not approved. Only the local Ollama catalog is allowed."
            )
        if model.runtime != "ollama" or not model.local_only or not model.supports_public_pool:
            raise PolicyError(
                f"Model '{model_tag}' is not eligible for the local-only public pool."
            )
        return model

    def normalize_selector(self, selector: str) -> str:
        normalized = selector.strip().lower()
        if not normalized:
            raise PolicyError("A model tag or quality selector is required.")
        if normalized in QUALITY_SELECTORS:
            return normalized
        self.require_local_model(selector)
        return selector

    def resolve_selector_for_models(
        self,
        selector: str,
        installed_models: set[str],
    ) -> ModelDefinition | None:
        normalized = self.normalize_selector(selector)
        candidates = [
            self.models[model_tag]
            for model_tag in installed_models
            if model_tag in self.models
        ]
        if normalized == "auto":
            return self._strongest_model(candidates)
        if normalized in QUALITY_SELECTORS:
            tier_candidates = [model for model in candidates if model.quality_tier == normalized]
            return self._strongest_model(tier_candidates)
        model = self.require_local_model(normalized)
        return model if model.tag in installed_models else None

    def estimate_reservation(
        self,
        selector: str,
        prompt_tokens: int,
        max_output_tokens: int,
    ) -> float:
        normalized = self.normalize_selector(selector)
        if normalized in QUALITY_SELECTORS:
            candidates = self._candidate_models_for_selector(normalized)
            model = max(
                candidates,
                key=lambda candidate: candidate.estimate_credits(
                    prompt_tokens=prompt_tokens,
                    output_tokens=max_output_tokens,
                ),
            )
            base = model.estimate_credits(prompt_tokens=prompt_tokens, output_tokens=max_output_tokens)
            return round(base * QUALITY_MULTIPLIERS[normalized], 4)
        model = self.require_local_model(normalized)
        return model.estimate_credits(prompt_tokens=prompt_tokens, output_tokens=max_output_tokens)

    def actual_cost(
        self,
        selector: str,
        resolved_model_tag: str,
        prompt_tokens: int,
        output_tokens: int,
    ) -> float:
        model = self.require_local_model(resolved_model_tag)
        base = model.estimate_credits(prompt_tokens=prompt_tokens, output_tokens=output_tokens)
        normalized = self.normalize_selector(selector)
        if normalized in QUALITY_SELECTORS:
            return round(base * QUALITY_MULTIPLIERS[normalized], 4)
        return base

    def _candidate_models_for_selector(self, selector: str) -> list[ModelDefinition]:
        if selector == "auto":
            return list(self.models.values())
        if selector in QUALITY_SELECTORS:
            return [model for model in self.models.values() if model.quality_tier == selector]
        return [self.require_local_model(selector)]

    @staticmethod
    def _strongest_model(models: list[ModelDefinition]) -> ModelDefinition | None:
        if not models:
            return None
        return max(models, key=lambda model: (model.strength_score, model.min_vram_gb))
