"""Tests for rapyd.webhooks — webhook signature verification and event parsing."""

import base64
import hashlib
import hmac as _hmac
import json

import pytest

from rapyd.exceptions import RapydWebhookError
from rapyd.models.payment import Payment
from rapyd.webhooks import WebhookHandler, parse_webhook_event


AK = "ak_test"
SK = "sk_test"
URL = "https://example.com/webhook"


def _make_signature(body_string: str, salt: str, timestamp: str) -> str:
    to_sign = URL + salt + timestamp + AK + SK + body_string
    raw = _hmac.new(SK.encode(), to_sign.encode(), hashlib.sha256).digest()
    return base64.b64encode(raw.hex().encode()).decode()


def test_valid_signature_parses_event():
    payload = json.dumps({
        "id": "wh_123",
        "type": "PAYMENT_COMPLETED",
        "data": {"id": "payment_abc", "amount": 100.0, "status": "CLO"},
        "trigger_operation_id": "op_1",
        "status": "NEW",
        "created_at": 1700000000,
    })
    salt = "webhooksalt1"
    ts = "1700000000"
    sig = _make_signature(payload, salt, ts)

    event = parse_webhook_event(
        payload,
        salt=salt,
        timestamp=ts,
        signature=sig,
        access_key=AK,
        secret_key=SK,
        webhook_url=URL,
    )

    assert event.id == "wh_123"
    assert event.type == "PAYMENT_COMPLETED"
    assert isinstance(event.data, Payment)
    assert event.data.id == "payment_abc"
    assert event.data.amount == 100.0


def test_tampered_body_raises_error():
    payload = json.dumps({"id": "wh_123", "type": "PAYMENT_COMPLETED", "data": {}})
    salt = "webhooksalt1"
    ts = "1700000000"
    sig = _make_signature(payload, salt, ts)

    # Tamper with the body
    tampered = json.dumps({"id": "wh_123", "type": "PAYMENT_COMPLETED", "data": {"amount": 999}})

    with pytest.raises(RapydWebhookError, match="Invalid webhook signature"):
        parse_webhook_event(
            tampered,
            salt=salt,
            timestamp=ts,
            signature=sig,
            access_key=AK,
            secret_key=SK,
            webhook_url=URL,
        )


def test_unknown_event_type_returns_dict_data():
    payload = json.dumps({
        "id": "wh_456",
        "type": "SOME_FUTURE_EVENT",
        "data": {"foo": "bar"},
        "trigger_operation_id": "op_2",
        "status": "NEW",
        "created_at": 1700000000,
    })
    salt = "salt12345678"
    ts = "1700000000"
    sig = _make_signature(payload, salt, ts)

    event = parse_webhook_event(
        payload,
        salt=salt,
        timestamp=ts,
        signature=sig,
        access_key=AK,
        secret_key=SK,
        webhook_url=URL,
    )

    assert event.type == "SOME_FUTURE_EVENT"
    assert isinstance(event.data, dict)
    assert event.data["foo"] == "bar"


async def test_webhook_handler_dispatch():
    handler = WebhookHandler()
    received = []

    @handler.on("PAYMENT_COMPLETED")
    async def on_payment(event):
        received.append(event)

    from rapyd.models.webhook import WebhookEvent

    event = WebhookEvent(id="wh_1", type="PAYMENT_COMPLETED", data={"id": "p1"})
    await handler.dispatch(event)

    assert len(received) == 1
    assert received[0].id == "wh_1"
