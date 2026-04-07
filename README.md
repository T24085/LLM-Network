# LLM Network

MVP for a reciprocal decentralized inference network built around local-only Ollama workers.

## Goals

- only local Ollama models
- no cloud model fallback
- users earn credits by serving verified public jobs
- users spend those credits to use other people's machines
- self-farming is blocked by scheduler policy

## Project Layout

- `src/ollama_network/`: coordinator, ledger, model catalog, and demo
- `tests/`: focused policy and accounting tests
- `LLM_NETWORK_MVP.md`: architecture notes and next-step roadmap

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

## Run

```bash
python -m ollama_network.demo
```

Run the API server:

```bash
python -m ollama_network.server --host 127.0.0.1 --port 8000
```

Windows quickstart:

```bat
quickstart_demo.bat
quickstart_demo.bat worker
```

Open the dashboard:

```text
http://127.0.0.1:8000/dashboard
```

Use the CLI instead of the dashboard:

```bash
python -m ollama_network.cli --server-url http://127.0.0.1:8000 models
python -m ollama_network.cli --server-url http://127.0.0.1:8000 issue-user --starting-credits 5
python -m ollama_network.cli --server-url http://127.0.0.1:8000 user --user-id usr_your_id_here
python -m ollama_network.cli --server-url http://127.0.0.1:8000 submit-job --requester-user-id usr_your_id_here --model-tag qwen3:4b --prompt "Summarize the worker protocol." --max-output-tokens 240
```

Run a worker daemon against that server:

```bash
python -m ollama_network.worker_daemon --server-url http://127.0.0.1:8000 --worker-id worker-bob-01 --owner-user-id bob --gpu-name "RTX 4090" --vram-gb 24 --model llama3.1:8b --tps llama3.1:8b=72
```

The dashboard can also:

- issue opaque user identifiers and look them up later
- start and stop a same-machine local worker loop with one button
- submit jobs to the local coordinator
- inspect balances, queue depth, jobs, and worker state
- generate copyable CLI commands from the current form values

That last action is intentionally an MVP convenience. It is useful for development and single-host testing, but it is not the long-term shape of a real distributed worker fleet.

Private local state is stored in:

`[.runtime/private_state.json](C:\Users\edchr\OneDrive\Desktop\Taylor\MachineLearningDesign\LLM%20Network\.runtime\private_state.json)`

That file is used only by the local server process. It is not exposed by the dashboard as a public download or static asset.

## Test

```bash
pytest
```
