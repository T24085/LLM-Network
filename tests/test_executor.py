from types import SimpleNamespace

from ollama_network.executor import OllamaCommandExecutor


def test_ollama_executor_builds_local_run_command(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_run(command, capture_output, text, timeout, check):
        captured["command"] = command
        captured["capture_output"] = capture_output
        captured["text"] = text
        captured["timeout"] = timeout
        captured["check"] = check
        return SimpleNamespace(returncode=0, stdout="hello from ollama", stderr="")

    monkeypatch.setattr("ollama_network.executor.subprocess.run", fake_run)

    executor = OllamaCommandExecutor(timeout_seconds=12)
    result = executor.run(
        model_tag="llama3.1:8b",
        prompt="Draft a network note.",
        max_output_tokens=120,
    )

    assert captured["command"][0:3] == ["ollama", "run", "llama3.1:8b"]
    assert "Respond in no more than 120 tokens." in captured["command"][3]
    assert result.success is True
    assert result.output_text == "hello from ollama"
    assert result.output_tokens > 0


def test_ollama_executor_sanitizes_ansi_and_thinking_output(monkeypatch) -> None:
    def fake_run(command, capture_output, text, timeout, check):
        return SimpleNamespace(
            returncode=0,
            stdout=(
                "Thinking...\n"
                "drafting\n"
                "...done thinking.\n\n"
                "Final answer here.\x1b[3D\x1b[K"
            ),
            stderr="",
        )

    monkeypatch.setattr("ollama_network.executor.subprocess.run", fake_run)

    executor = OllamaCommandExecutor(timeout_seconds=12)
    result = executor.run(
        model_tag="qwen3:4b",
        prompt="Test output cleanup.",
        max_output_tokens=80,
    )

    assert result.success is True
    assert result.output_text == "Final answer here."
    assert "\x1b" not in result.output_text
