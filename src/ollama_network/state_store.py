from __future__ import annotations

import json
from pathlib import Path
from time import sleep


class LocalStateStore:
    """Persists coordinator state to a local JSON file that is never served by the API."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> dict[str, object] | None:
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, payload: dict[str, object]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        encoded = json.dumps(payload, indent=2)
        temp_path.write_text(encoded, encoding="utf-8")
        for _ in range(3):
            try:
                temp_path.replace(self.path)
                return
            except PermissionError:
                sleep(0.05)
        # Fall back to a direct write when Windows or sync clients briefly lock replace().
        self.path.write_text(encoded, encoding="utf-8")
        if temp_path.exists():
            temp_path.unlink()
