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
pip install -r requirements-dev.txt
```

If you prefer installing from project metadata directly:

```bash
pip install -e .[dev]
```

## Run

```bash
python -m ollama_network.demo
```

Run the API server:

```bash
python -m ollama_network.server --host localhost --port 8000
```

If you want other machines on your LAN or over the internet to reach the server, bind it to every interface instead:

```bash
python -m ollama_network.server --host 0.0.0.0 --port 8000
```

If you want Google sign-in locally, keep the Firebase web config out of git and provide it either through environment variables or an untracked file at `.runtime/firebase.local.json`.

Example:

```json
{
  "apiKey": "your-rotated-firebase-web-api-key",
  "authDomain": "llm-network.firebaseapp.com",
  "projectId": "llm-network",
  "storageBucket": "llm-network.firebasestorage.app",
  "messagingSenderId": "502332096634",
  "appId": "1:502332096634:web:bc43239838ae06ef197bc3"
}
```

If you want shared conversations, balances, bindings, and history across machines, configure the server to use Firestore instead of the local JSON file:

```powershell
$env:OLLAMA_NETWORK_STATE_BACKEND="firestore"
$env:OLLAMA_NETWORK_FIRESTORE_PROJECT_ID="your-project-id"
$env:OLLAMA_NETWORK_FIRESTORE_COLLECTION="ollama_network_state"
$env:OLLAMA_NETWORK_FIRESTORE_DOCUMENT="shared"
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service-account.json"
```

Rules by themselves are not enough for this server-side sync path. The backend must write to Firestore using server credentials, which is what the optional Firestore state backend does.

Windows quickstart:

```bat
start_network_server.bat
start_dashboard.bat
```

Open the dashboard:

```text
http://localhost:8000/dashboard
```

Use the CLI instead of the dashboard:

```bash
python -m ollama_network.cli --server-url http://localhost:8000 models
python -m ollama_network.cli --server-url http://localhost:8000 issue-user --starting-credits 5
python -m ollama_network.cli --server-url http://localhost:8000 user --user-id usr_your_id_here
python -m ollama_network.cli --server-url http://localhost:8000 submit-job --requester-user-id usr_your_id_here --model-tag qwen3:4b --prompt "Summarize the worker protocol." --max-output-tokens 240
```

Run a worker daemon against that server:

```bash
python -m ollama_network.worker_daemon --server-url http://localhost:8000 --worker-id worker-bob-01 --owner-user-id bob --gpu-name "RTX 4090" --vram-gb 24 --model llama3.1:8b --tps llama3.1:8b=72 --worker-token YOUR_WORKER_TOKEN
```

## Remote Workers

The intended shape is:

- your main PC runs the coordinator API server
- browsers connect to that server over the dashboard
- remote machines such as a Jetson Nano run `worker_daemon`
- worker daemons authenticate with a long-lived worker token, not a short-lived Firebase browser token

Issue a worker token on the coordinator host:

```bash
python -m ollama_network.cli issue-worker-token --user-id usr_your_id_here --label jetson-nano-home
```

That command writes the token metadata into the coordinator's private local state and prints the raw token once. Keep it secret.

List or revoke tokens later from the coordinator host:

```bash
python -m ollama_network.cli list-worker-tokens --user-id usr_your_id_here
python -m ollama_network.cli revoke-worker-token --user-id usr_your_id_here --token-id wkt_your_token_id
```

Example Jetson Nano daemon command:

```bash
python3 -m ollama_network.worker_daemon \
  --server-url http://YOUR_MAIN_PC_IP:8000 \
  --worker-id worker-jetson-nano-01 \
  --owner-user-id usr_your_id_here \
  --gpu-name "Jetson Nano" \
  --vram-gb 4 \
  --model qwen3:4b \
  --tps qwen3:4b=10 \
  --worker-token YOUR_WORKER_TOKEN
```

For a real multi-machine deployment:

- add your public hostname to Firebase Authentication -> Authorized domains
- serve the coordinator behind HTTPS before exposing it outside your home LAN
- forward TCP `8000` from your router only if you understand the exposure and trust the machine
- prefer a reverse proxy or tunnel in front of the Python server instead of exposing the raw port directly
- the Jetson should point at the public base URL or LAN IP of the coordinator, not `localhost`

## GitHub Bootstrap

Yes. A single `curl | bash` bootstrap can be served straight from GitHub using the raw file URL after the script is pushed.

Client install example:

```bash
curl -fsSL https://raw.githubusercontent.com/T24085/LLM-Network/main/scripts/bootstrap_linux.sh | \
  bash -s -- --server-url http://YOUR_MAIN_PC_IP:8000
```

That installs the same user-facing CLI environment everyone needs. The same account can submit jobs and also own workers.

Jetson worker enablement example from the same script:

```bash
curl -fsSL https://raw.githubusercontent.com/T24085/LLM-Network/main/scripts/bootstrap_linux.sh | \
  bash -s -- \
    --server-url http://YOUR_MAIN_PC_IP:8000 \
    --enable-worker \
    --owner-user-id usr_your_id_here \
    --worker-id worker-jetson-nano-01 \
    --gpu-name "Jetson Nano" \
    --vram-gb 4 \
    --models qwen3:4b \
    --tps qwen3:4b=10 \
    --worker-token YOUR_WORKER_TOKEN
```

The bootstrap script lives at:

`scripts/bootstrap_linux.sh`

What it does:

- installs Python prerequisites if possible
- creates a dedicated virtual environment under `~/.llm-network`
- installs the package from GitHub
- always installs the client and CLI tools
- enables worker mode automatically when worker flags are supplied or `--enable-worker` is used
- installs Ollama automatically for worker nodes when Ollama is missing
- optionally pulls the requested Ollama models
- writes a reusable worker launcher
- writes `~/open_llm_network_dashboard.sh` and a Linux desktop shortcut when a desktop environment is present
- writes `~/start_llm_network_worker.sh` when worker mode is enabled
- installs and starts a systemd worker service when `systemctl` and `sudo` are available

The dashboard can also:

- issue opaque user identifiers and look them up later
- start and stop a same-machine local worker loop with one button
- submit jobs to the local coordinator
- inspect balances, queue depth, jobs, and worker state
- generate copyable CLI commands from the current form values

That last action is intentionally an MVP convenience. It is useful for development and single-host testing, but it is not the long-term shape of a real distributed worker fleet.

Private local state is stored in:

`D:\LLM-Network\.runtime\private_state.json`

That file is used only by the local server process. It is not exposed by the dashboard as a public download or static asset.

## Test

```bash
pytest
```
