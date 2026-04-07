from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .dashboard import DASHBOARD_HTML
from .models import PolicyError
from .service import NetworkService, handle_policy_error


class NetworkHTTPServer(ThreadingHTTPServer):
    service: NetworkService

    def __init__(self, server_address: tuple[str, int], service: NetworkService) -> None:
        super().__init__(server_address, NetworkAPIHandler)
        self.service = service


class NetworkAPIHandler(BaseHTTPRequestHandler):
    server: NetworkHTTPServer

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        try:
            if path in {"/", "/dashboard"}:
                self._write_html(HTTPStatus.OK, DASHBOARD_HTML)
                return
            if path == "/health":
                self._write_json(HTTPStatus.OK, {"status": "ok"})
                return
            if path == "/models":
                self._write_json(HTTPStatus.OK, self.server.service.list_models())
                return
            if path == "/identity-context":
                self._write_json(HTTPStatus.OK, self.server.service.get_identity_context())
                return
            if path == "/worker-context":
                self._write_json(HTTPStatus.OK, self.server.service.get_worker_context())
                return
            if path == "/network":
                self._write_json(HTTPStatus.OK, self.server.service.get_network())
                return
            if path.startswith("/users/"):
                user_id = path.split("/", maxsplit=2)[2]
                self._write_json(HTTPStatus.OK, self.server.service.get_user(user_id))
                return
            if path.startswith("/jobs/"):
                job_id = path.split("/", maxsplit=2)[2]
                self._write_json(HTTPStatus.OK, self.server.service.get_job(job_id))
                return
            self._write_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
        except KeyError:
            self._write_json(HTTPStatus.NOT_FOUND, {"error": "unknown resource"})
        except PolicyError as error:
            status, payload = handle_policy_error(error)
            self._write_json(status, payload)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        try:
            payload = self._read_json_body()
            if path == "/users/issue":
                result = self.server.service.issue_user_identity(
                    starting_credits=float(payload.get("starting_credits", 0.0)),
                )
                self._write_json(HTTPStatus.CREATED, result)
                return
            if path == "/users/register":
                result = self.server.service.register_user(
                    user_id=str(payload["user_id"]),
                    starting_credits=float(payload.get("starting_credits", 0.0)),
                )
                self._write_json(HTTPStatus.CREATED, result)
                return
            if path == "/workers/register":
                self._write_json(HTTPStatus.CREATED, self.server.service.register_worker(payload))
                return
            if path == "/workers/start-local":
                self._write_json(HTTPStatus.CREATED, self.server.service.start_local_worker(payload))
                return
            if path.startswith("/workers/") and path.endswith("/claim"):
                worker_id = path.split("/")[2]
                assignment = self.server.service.claim_job_for_worker(worker_id)
                if assignment is None:
                    self._write_json(HTTPStatus.OK, {"assignment": None})
                    return
                self._write_json(HTTPStatus.OK, {"assignment": assignment})
                return
            if path.startswith("/workers/") and path.endswith("/stop-local"):
                worker_id = path.split("/")[2]
                self._write_json(HTTPStatus.OK, {"loop": self.server.service.stop_local_worker(worker_id)})
                return
            if path.startswith("/workers/") and path.endswith("/run-once"):
                worker_id = path.split("/")[2]
                result = self.server.service.run_worker_cycle(worker_id)
                if result is None:
                    self._write_json(HTTPStatus.OK, {"job": None})
                    return
                self._write_json(HTTPStatus.OK, {"job": result})
                return
            if path == "/jobs":
                self._write_json(HTTPStatus.CREATED, self.server.service.submit_job(payload))
                return
            if path == "/jobs/complete":
                self._write_json(HTTPStatus.OK, self.server.service.complete_job(payload))
                return
            self._write_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
        except json.JSONDecodeError:
            self._write_json(HTTPStatus.BAD_REQUEST, {"error": "invalid json"})
        except KeyError as error:
            self._write_json(HTTPStatus.BAD_REQUEST, {"error": f"missing field: {error.args[0]}"})
        except PolicyError as error:
            status, body = handle_policy_error(error)
            self._write_json(status, body)
        except ValueError as error:
            self._write_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})

    def log_message(self, format: str, *args: object) -> None:
        return

    def _read_json_body(self) -> dict[str, object]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length else b"{}"
        parsed = json.loads(raw.decode("utf-8"))
        if not isinstance(parsed, dict):
            raise ValueError("JSON body must be an object.")
        return parsed

    def _write_json(self, status: int | HTTPStatus, payload: dict[str, object]) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _write_html(self, status: int | HTTPStatus, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def create_server(host: str = "127.0.0.1", port: int = 8000) -> NetworkHTTPServer:
    service = NetworkService()
    return NetworkHTTPServer((host, port), service=service)
