"""Token QR opachi e autenticati tramite HMAC-SHA256."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
from pathlib import Path
import secrets

from fastcharge.paths import secret_key_path


PREFIX = "fastcharge:v1"


def load_or_create_secret(path: Path | None = None) -> bytes:
    configured = os.getenv("QR_SIGNING_SECRET")
    if configured:
        return configured.encode("utf-8")
    target = path or secret_key_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        return target.read_bytes()
    except FileNotFoundError:
        key = secrets.token_bytes(32)
        try:
            descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            return target.read_bytes()
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(key)
        return key


def create_token(user_id: str, secret: bytes | None = None) -> str:
    payload = f"{PREFIX}:{user_id}"
    signature = hmac.new(secret or load_or_create_secret(), payload.encode(), hashlib.sha256).digest()
    encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return f"{payload}:{encoded}"


def verify_token(token: str, secret: bytes | None = None) -> str | None:
    try:
        prefix, version, user_id, supplied = token.split(":", 3)
    except ValueError:
        return None
    if f"{prefix}:{version}" != PREFIX or not user_id:
        return None
    expected = create_token(user_id, secret).rsplit(":", 1)[1]
    return user_id if hmac.compare_digest(supplied, expected) else None
