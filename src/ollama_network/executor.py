from __future__ import annotations

import re
import subprocess
import time

from .models import ExecutorResult


class OllamaCommandExecutor:
    """Executes local-only inference through the Ollama CLI."""

    _ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    _THINKING_MARKERS = ("...done thinking.", "</think>")

    def __init__(self, ollama_binary: str = "ollama", timeout_seconds: float = 180.0) -> None:
        self.ollama_binary = ollama_binary
        self.timeout_seconds = timeout_seconds

    def run(self, model_tag: str, prompt: str, max_output_tokens: int) -> ExecutorResult:
        start = time.perf_counter()
        constrained_prompt = (
            f"{prompt}\n\nRespond in no more than {max_output_tokens} tokens."
        )
        try:
            completed = subprocess.run(
                [self.ollama_binary, "run", model_tag, constrained_prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            return ExecutorResult(
                success=False,
                output_text="",
                output_tokens=0,
                latency_seconds=time.perf_counter() - start,
                verified=False,
                error_message=f"Ollama timed out after {self.timeout_seconds:.0f}s: {error}",
            )
        success = completed.returncode == 0
        output_text = self._sanitize_output(completed.stdout)
        error_message = "" if success else completed.stderr.strip() or "ollama run failed"
        return ExecutorResult(
            success=success,
            output_text=output_text,
            output_tokens=self._estimate_tokens(output_text),
            latency_seconds=time.perf_counter() - start,
            verified=success,
            error_message=error_message,
        )

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return max(1, int(len([token for token in text.split() if token.strip()]) * 1.3)) if text else 0

    @classmethod
    def _sanitize_output(cls, text: str) -> str:
        cleaned = cls._ANSI_ESCAPE_RE.sub("", text or "")
        cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n").strip()
        cleaned = cls._strip_thinking_block(cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

    @classmethod
    def _strip_thinking_block(cls, text: str) -> str:
        if not text:
            return ""
        think_match = re.search(r"<think>.*?</think>\s*", text, flags=re.DOTALL | re.IGNORECASE)
        if think_match:
            stripped = (text[: think_match.start()] + text[think_match.end() :]).strip()
            return stripped or text
        lowered = text.lower()
        for marker in cls._THINKING_MARKERS:
            marker_index = lowered.rfind(marker)
            if marker_index >= 0:
                stripped = text[marker_index + len(marker) :].strip()
                return stripped or text
        return text
