from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable, TextIO
from urllib import error, request

from .worker_daemon import parse_throughput


def _http_request(
    server_url: str,
    path: str,
    method: str,
    payload: dict[str, object] | None = None,
) -> dict[str, object]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=f"{server_url.rstrip('/')}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except error.HTTPError as http_error:
        detail = http_error.read().decode("utf-8")
        raise RuntimeError(f"{http_error.code} {detail}") from http_error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI for the Ollama Network local coordinator.")
    parser.add_argument(
        "--server-url",
        default="http://127.0.0.1:8000",
        help="Coordinator API base URL.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    issue_user = subparsers.add_parser("issue-user", help="Issue a new opaque user identifier.")
    issue_user.add_argument("--starting-credits", type=float, default=0.0)

    register_user = subparsers.add_parser("register-user", help="Register a user.")
    register_user.add_argument("--user-id", required=True)
    register_user.add_argument("--starting-credits", type=float, default=0.0)

    user = subparsers.add_parser("user", help="Fetch a user balance.")
    user.add_argument("--user-id", required=True)

    subparsers.add_parser("models", help="List approved Ollama models.")
    subparsers.add_parser("network", help="Fetch the network snapshot.")

    job = subparsers.add_parser("job", help="Fetch a single job.")
    job.add_argument("--job-id", required=True)

    submit_job = subparsers.add_parser("submit-job", help="Submit a job.")
    submit_job.add_argument("--requester-user-id", required=True)
    submit_job.add_argument(
        "--model-tag",
        required=True,
        help="Exact approved tag or one of: auto, good, better, best.",
    )
    submit_job.add_argument("--prompt", required=True)
    submit_job.add_argument("--max-output-tokens", type=int, required=True)
    submit_job.add_argument("--prompt-tokens", type=int)

    register_worker = subparsers.add_parser("register-worker", help="Register a worker.")
    register_worker.add_argument("--worker-id", required=True)
    register_worker.add_argument("--owner-user-id", required=True)
    register_worker.add_argument("--gpu-name", required=True)
    register_worker.add_argument("--vram-gb", type=float, required=True)
    register_worker.add_argument("--model", action="append", dest="models", required=True)
    register_worker.add_argument(
        "--tps",
        action="append",
        dest="throughput_entries",
        default=[],
        help="Throughput entry in MODEL=TPS format. Repeatable.",
    )

    claim_job = subparsers.add_parser("claim-job", help="Claim the next job for a worker.")
    claim_job.add_argument("--worker-id", required=True)

    run_once = subparsers.add_parser(
        "run-worker-once",
        help="Run one worker cycle through the API server.",
    )
    run_once.add_argument("--worker-id", required=True)

    return parser


def run_cli(argv: Iterable[str] | None = None, stdout: TextIO | None = None) -> dict[str, object]:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    stdout = stdout or sys.stdout

    if args.command == "issue-user":
        result = _http_request(
            args.server_url,
            "/users/issue",
            "POST",
            {
                "starting_credits": args.starting_credits,
            },
        )
    elif args.command == "register-user":
        result = _http_request(
            args.server_url,
            "/users/register",
            "POST",
            {
                "user_id": args.user_id,
                "starting_credits": args.starting_credits,
            },
        )
    elif args.command == "user":
        result = _http_request(args.server_url, f"/users/{args.user_id}", "GET")
    elif args.command == "models":
        result = _http_request(args.server_url, "/models", "GET")
    elif args.command == "network":
        result = _http_request(args.server_url, "/network", "GET")
    elif args.command == "job":
        result = _http_request(args.server_url, f"/jobs/{args.job_id}", "GET")
    elif args.command == "submit-job":
        payload = {
            "requester_user_id": args.requester_user_id,
            "model_tag": args.model_tag,
            "prompt": args.prompt,
            "max_output_tokens": args.max_output_tokens,
        }
        if args.prompt_tokens is not None:
            payload["prompt_tokens"] = args.prompt_tokens
        result = _http_request(args.server_url, "/jobs", "POST", payload)
    elif args.command == "register-worker":
        payload = {
            "worker_id": args.worker_id,
            "owner_user_id": args.owner_user_id,
            "gpu_name": args.gpu_name,
            "vram_gb": args.vram_gb,
            "installed_models": args.models,
            "benchmark_tokens_per_second": parse_throughput(
                args.throughput_entries,
                args.models,
            ),
            "runtime": "ollama",
            "allows_cloud_fallback": False,
        }
        result = _http_request(args.server_url, "/workers/register", "POST", payload)
    elif args.command == "claim-job":
        result = _http_request(
            args.server_url,
            f"/workers/{args.worker_id}/claim",
            "POST",
            {},
        )
    elif args.command == "run-worker-once":
        result = _http_request(
            args.server_url,
            f"/workers/{args.worker_id}/run-once",
            "POST",
            {},
        )
    else:
        raise RuntimeError(f"Unsupported command: {args.command}")

    stdout.write(json.dumps(result, indent=2))
    stdout.write("\n")
    return result


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()
