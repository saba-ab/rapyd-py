"""Tests for rapyd.http — async HTTP client."""

import pytest
import httpx
from pytest_httpx import HTTPXMock

from rapyd.config import RapydSettings
from rapyd.exceptions import RapydApiError, RapydAuthError, RapydTimeoutError
from rapyd.http import RapydHttpClient


def _settings() -> RapydSettings:
    return RapydSettings(rapyd_access_key="ak_test", rapyd_secret_key="sk_test")


def _success_response(data: dict | list | None = None) -> dict:
    return {
        "status": {
            "error_code": "",
            "status": "SUCCESS",
            "message": "",
            "response_code": "",
            "operation_id": "op_123",
        },
        "data": data or {},
    }


def _error_response(
    error_code: str = "GENERAL_ERROR",
    message: str = "Something went wrong",
    status: str = "ERROR",
) -> dict:
    return {
        "status": {
            "error_code": error_code,
            "status": status,
            "message": message,
            "response_code": "",
            "operation_id": "op_err",
        },
        "data": None,
    }


async def test_get_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=_success_response({"id": "payment_123"}))

    async with RapydHttpClient(_settings()) as client:
        result = await client.get("/v1/payments/payment_123")

    assert result["data"]["id"] == "payment_123"
    assert result["status"]["status"] == "SUCCESS"


async def test_post_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=_success_response({"id": "payment_new"}))

    async with RapydHttpClient(_settings()) as client:
        result = await client.post("/v1/payments", body={"amount": 100, "currency": "USD"})

    assert result["data"]["id"] == "payment_new"
    # Verify idempotency header was sent
    request = httpx_mock.get_request()
    assert "idempotency" in request.headers


async def test_error_response_raises_api_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=400,
        json=_error_response("INVALID_PARAMETER", "amount is required"),
    )

    async with RapydHttpClient(_settings()) as client:
        with pytest.raises(RapydApiError) as exc_info:
            await client.post("/v1/payments", body={})

    assert exc_info.value.error_code == "INVALID_PARAMETER"
    assert exc_info.value.message == "amount is required"
    assert exc_info.value.status_code == 400


async def test_401_raises_auth_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=401,
        json=_error_response("UNAUTHORIZED_API_CALL", "Invalid access key"),
    )

    async with RapydHttpClient(_settings()) as client:
        with pytest.raises(RapydAuthError) as exc_info:
            await client.get("/v1/payments")

    assert isinstance(exc_info.value, RapydApiError)
    assert exc_info.value.status_code == 401


async def test_timeout_raises_timeout_error(httpx_mock: HTTPXMock):
    httpx_mock.add_exception(httpx.ReadTimeout("timed out"))

    async with RapydHttpClient(_settings()) as client:
        with pytest.raises(RapydTimeoutError):
            await client.get("/v1/payments")


async def test_put_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=_success_response({"id": "payment_123", "description": "updated"}))

    async with RapydHttpClient(_settings()) as client:
        result = await client.put("/v1/payments/payment_123", body={"description": "updated"})

    assert result["data"]["description"] == "updated"


async def test_delete_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=_success_response({"id": "payment_123", "status": "CAN"}))

    async with RapydHttpClient(_settings()) as client:
        result = await client.delete("/v1/payments/payment_123")

    assert result["data"]["status"] == "CAN"
