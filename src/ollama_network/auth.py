from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


class AuthenticationError(PermissionError):
    """Raised when a request is missing or carries an invalid Firebase token."""


@dataclass(frozen=True)
class FirebaseProjectConfig:
    api_key: str
    auth_domain: str
    project_id: str
    storage_bucket: str
    messaging_sender_id: str
    app_id: str

    def to_web_dict(self) -> dict[str, str]:
        return {
            "apiKey": self.api_key,
            "authDomain": self.auth_domain,
            "projectId": self.project_id,
            "storageBucket": self.storage_bucket,
            "messagingSenderId": self.messaging_sender_id,
            "appId": self.app_id,
        }

    def to_web_json(self) -> str:
        return json.dumps(self.to_web_dict())


def load_firebase_project_config() -> FirebaseProjectConfig:
    return FirebaseProjectConfig(
        api_key=os.environ.get("OLLAMA_NETWORK_FIREBASE_API_KEY", "AIzaSyBtO5ayrBMrc2irr-u-w4BOTZRlVEI67dM"),
        auth_domain=os.environ.get("OLLAMA_NETWORK_FIREBASE_AUTH_DOMAIN", "llm-network.firebaseapp.com"),
        project_id=os.environ.get("OLLAMA_NETWORK_FIREBASE_PROJECT_ID", "llm-network"),
        storage_bucket=os.environ.get("OLLAMA_NETWORK_FIREBASE_STORAGE_BUCKET", "llm-network.firebasestorage.app"),
        messaging_sender_id=os.environ.get("OLLAMA_NETWORK_FIREBASE_MESSAGING_SENDER_ID", "502332096634"),
        app_id=os.environ.get("OLLAMA_NETWORK_FIREBASE_APP_ID", "1:502332096634:web:bc43239838ae06ef197bc3"),
    )


class GoogleFirebaseTokenVerifier:
    """Validates Firebase ID tokens against Google public keys."""

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    def verify(self, token: str) -> dict[str, Any]:
        try:
            from google.auth.transport import requests as google_requests
            from google.oauth2 import id_token
        except ImportError as error:
            raise AuthenticationError(
                "Firebase auth support requires the 'google-auth' package to be installed."
            ) from error

        try:
            payload = id_token.verify_firebase_token(
                token,
                google_requests.Request(),
                audience=self.project_id,
            )
        except Exception as error:  # pragma: no cover - depends on external verifier behavior
            raise AuthenticationError("Your login token could not be verified.") from error

        if not payload:
            raise AuthenticationError("Your login token could not be verified.")

        issuer = str(payload.get("iss", ""))
        expected_issuer = f"https://securetoken.google.com/{self.project_id}"
        if issuer != expected_issuer:
            raise AuthenticationError("Your login token belongs to a different Firebase project.")

        uid = str(payload.get("uid") or payload.get("user_id") or "")
        if not uid:
            raise AuthenticationError("Your login token is missing a Firebase user id.")

        payload["uid"] = uid
        return payload
