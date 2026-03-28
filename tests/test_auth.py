"""Tests for rapyd.auth — request signing and webhook verification."""

from rapyd.auth import (
    _compact_json,
    _random_salt,
    sign_request,
    verify_webhook_signature,
)


def test_random_salt_length():
    salt = _random_salt(12)
    assert len(salt) == 12
    assert salt.isalnum()


def test_compact_json_with_dict():
    result = _compact_json({"amount": 100, "currency": "USD"})
    assert result == '{"amount":100,"currency":"USD"}'


def test_compact_json_none_returns_empty():
    assert _compact_json(None) == ""


def test_compact_json_empty_dict_returns_empty():
    assert _compact_json({}) == ""


def test_sign_request_deterministic():
    """Signing the same input twice with fixed salt/ts produces the same signature."""
    params = dict(
        http_method="post",
        url_path="/v1/payments",
        access_key="ak_test_123",
        secret_key="sk_test_456",
        body={"amount": 100, "currency": "USD"},
        salt="abcdefghijkl",
        timestamp="1700000000",
    )
    sig1 = sign_request(**params)
    sig2 = sign_request(**params)
    assert sig1["signature"] == sig2["signature"]
    assert sig1["salt"] == "abcdefghijkl"
    assert sig1["timestamp"] == "1700000000"


def test_sign_request_get_no_body():
    """GET request with no body uses empty body string."""
    result = sign_request(
        http_method="get",
        url_path="/v1/payments",
        access_key="ak",
        secret_key="sk",
        body=None,
        salt="salt12345678",
        timestamp="1700000000",
    )
    assert result["signature"]  # non-empty
    # Verify it differs from a POST with a body
    result2 = sign_request(
        http_method="post",
        url_path="/v1/payments",
        access_key="ak",
        secret_key="sk",
        body={"amount": 1},
        salt="salt12345678",
        timestamp="1700000000",
    )
    assert result["signature"] != result2["signature"]


def test_sign_request_signature_is_base64_of_hex():
    """Verify the signature is base64(hex(hmac)) — not base64(raw bytes)."""
    import base64
    import hashlib
    import hmac as _hmac

    ak, sk = "ak_test", "sk_test"
    salt, ts = "randomsalt12", "1700000000"
    body_string = '{"amount":100}'
    to_sign = "post" + "/v1/payments" + salt + ts + ak + sk + body_string

    raw = _hmac.new(sk.encode(), to_sign.encode(), hashlib.sha256).digest()
    expected = base64.b64encode(raw.hex().encode()).decode()

    result = sign_request(
        http_method="post",
        url_path="/v1/payments",
        access_key=ak,
        secret_key=sk,
        body={"amount": 100},
        salt=salt,
        timestamp=ts,
    )
    assert result["signature"] == expected


def test_verify_webhook_signature_valid():
    """Valid webhook signature passes verification."""
    ak, sk = "ak_test", "sk_test"
    salt, ts = "webhooksalt1", "1700000000"
    body_string = '{"type":"PAYMENT_COMPLETED"}'
    url_path = "https://example.com/webhook"

    # Compute expected signature using webhook formula (no http_method)
    import base64
    import hashlib
    import hmac as _hmac

    to_sign = url_path + salt + ts + ak + sk + body_string
    raw = _hmac.new(sk.encode(), to_sign.encode(), hashlib.sha256).digest()
    sig = base64.b64encode(raw.hex().encode()).decode()

    assert verify_webhook_signature(
        url_path=url_path,
        salt=salt,
        timestamp=ts,
        signature=sig,
        access_key=ak,
        secret_key=sk,
        body_string=body_string,
    )


def test_verify_webhook_signature_wrong_secret():
    """Wrong secret key fails verification."""
    assert not verify_webhook_signature(
        url_path="https://example.com/webhook",
        salt="salt12345678",
        timestamp="1700000000",
        signature="badsignature",
        access_key="ak",
        secret_key="sk",
        body_string="{}",
    )
