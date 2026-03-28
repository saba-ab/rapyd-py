"""Tests for PaymentsResource."""

import pytest
from pytest_httpx import HTTPXMock

from rapyd.exceptions import RapydApiError
from rapyd.models.payment import Payment
from rapyd.resources.payments import PaymentsResource
from tests.conftest import error_response, success_response


async def test_create_payment(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "payment_123",
        "amount": 100.0,
        "currency_code": "USD",
        "status": "ACT",
    }))

    resource = PaymentsResource(http_client)
    payment = await resource.create(amount=100.0, currency="USD")

    assert isinstance(payment, Payment)
    assert payment.id == "payment_123"
    assert payment.amount == 100.0


async def test_get_payment(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "payment_456",
        "amount": 50.0,
        "status": "CLO",
    }))

    resource = PaymentsResource(http_client)
    payment = await resource.get("payment_456")

    assert isinstance(payment, Payment)
    assert payment.id == "payment_456"


async def test_cancel_payment(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "payment_789",
        "status": "CAN",
    }))

    resource = PaymentsResource(http_client)
    payment = await resource.cancel("payment_789")

    assert payment.status == "CAN"
    request = httpx_mock.get_request()
    assert request.method == "DELETE"


async def test_list_payments(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response([
        {"id": "payment_1", "amount": 10.0},
        {"id": "payment_2", "amount": 20.0},
    ]))

    resource = PaymentsResource(http_client)
    payments = await resource.list(limit=10)

    assert len(payments) == 2
    assert all(isinstance(p, Payment) for p in payments)
    assert payments[0].id == "payment_1"


async def test_api_error_raises(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(
        status_code=400,
        json=error_response("INVALID_FIELDS", "amount is required"),
    )

    resource = PaymentsResource(http_client)
    with pytest.raises(RapydApiError) as exc_info:
        await resource.create()

    assert exc_info.value.error_code == "INVALID_FIELDS"


async def test_capture_payment(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "payment_cap",
        "captured": True,
    }))

    resource = PaymentsResource(http_client)
    payment = await resource.capture("payment_cap")

    assert payment.captured is True
    request = httpx_mock.get_request()
    assert "/capture" in request.url.path
