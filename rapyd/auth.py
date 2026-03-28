"""HMAC-SHA256 request signing and webhook signature verification for Rapyd API."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import random
import string
import time


def _random_salt(length: int = 12) -> str:
    """Generate a random alphanumeric salt string."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def _unix_timestamp() -> str:
    """Return the current Unix timestamp as a string."""
    return str(int(time.time()))


def _compact_json(body: dict | None) -> str:
    """Serialize body to compact JSON (no whitespace). Empty/None returns empty string."""
    if not body:
        return ""
    return json.dumps(body, separators=(",", ":"))


def _compute_signature(to_sign: str, secret_key: str) -> str:
    """HMAC-SHA256 -> hex string -> base64 encode."""
    raw = hmac.new(secret_key.encode(), to_sign.encode(), hashlib.sha256).digest()
    return base64.b64encode(raw.hex().encode()).decode()


def sign_request(
    *,
    http_method: str,
    url_path: str,
    access_key: str,
    secret_key: str,
    body: dict | None = None,
    salt: str | None = None,
    timestamp: str | None = None,
) -> dict[str, str]:
    """Sign a Rapyd API request.

    Returns a dict with keys: access_key, salt, timestamp, signature.
    """
    salt = salt or _random_salt()
    timestamp = timestamp or _unix_timestamp()
    body_string = _compact_json(body)

    to_sign = (
        http_method.lower()
        + url_path
        + salt
        + timestamp
        + access_key
        + secret_key
        + body_string
    )

    signature = _compute_signature(to_sign, secret_key)

    return {
        "access_key": access_key,
        "salt": salt,
        "timestamp": timestamp,
        "signature": signature,
    }


def verify_webhook_signature(
    *,
    url_path: str,
    salt: str,
    timestamp: str,
    signature: str,
    access_key: str,
    secret_key: str,
    body_string: str,
) -> bool:
    """Verify a Rapyd webhook signature (timing-safe).

    Webhook formula does NOT include http_method.
    """
    to_sign = url_path + salt + timestamp + access_key + secret_key + body_string
    expected = _compute_signature(to_sign, secret_key)
    return hmac.compare_digest(expected, signature)
