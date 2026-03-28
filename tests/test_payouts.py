"""Tests for PayoutsResource."""

from pytest_httpx import HTTPXMock

from rapyd.models.payout import Payout
from rapyd.resources.payouts import PayoutsResource
from tests.conftest import success_response


async def test_create_payout(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "payout_123",
        "payout_amount": 500.0,
        "payout_currency": "PHP",
        "status": "Created",
    }))

    resource = PayoutsResource(http_client)
    payout = await resource.create(payout_amount=500.0, payout_currency="PHP")

    assert isinstance(payout, Payout)
    assert payout.id == "payout_123"
    assert payout.payout_amount == 500.0


async def test_confirm_payout(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "payout_456",
        "status": "Completed",
    }))

    resource = PayoutsResource(http_client)
    payout = await resource.confirm("payout_456")

    assert payout.status == "Completed"
    request = httpx_mock.get_request()
    assert "/confirm/payout_456" in request.url.path


async def test_list_payouts(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response([
        {"id": "payout_1", "payout_amount": 100.0},
        {"id": "payout_2", "payout_amount": 200.0},
    ]))

    resource = PayoutsResource(http_client)
    payouts = await resource.list(limit=10)

    assert len(payouts) == 2
    assert all(isinstance(p, Payout) for p in payouts)


async def test_complete_payout(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "payout_789",
        "status": "Completed",
    }))

    resource = PayoutsResource(http_client)
    payout = await resource.complete("payout_789", 500.0)

    assert payout.status == "Completed"
    request = httpx_mock.get_request()
    assert "/complete/payout_789/500.0" in request.url.path
