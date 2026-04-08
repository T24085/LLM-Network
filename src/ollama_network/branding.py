from __future__ import annotations

import base64
import os
from functools import lru_cache
from pathlib import Path

DEFAULT_LOGO_PATH = Path(r"C:\Users\edchr\Downloads\LLM Network logo design.png")


@lru_cache(maxsize=1)
def load_logo_data_url() -> str:
    configured = os.environ.get("OLLAMA_NETWORK_LOGO_PATH", "").strip()
    path = Path(configured) if configured else DEFAULT_LOGO_PATH
    try:
        raw = path.read_bytes()
    except OSError:
        return ""
    suffix = path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg" if suffix in {".jpg", ".jpeg"} else "application/octet-stream"
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{encoded}"
