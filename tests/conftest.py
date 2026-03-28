"""Shared test fixtures."""

import os

import pytest

from rapyd.config import RapydSettings
from rapyd.http import RapydHttpClient


@pytest.fixture(autouse=True)
def _set_env(monkeypatch):
    """Ensure env vars are set for all tests."""
    monkeypatch.setenv("RAPYD_ACCESS_KEY", "ak_test")
    monkeypatch.setenv("RAPYD_SECRET_KEY", "sk_test")


@pytest.fixture
def settings():
    return RapydSettings(rapyd_access_key="ak_test", rapyd_secret_key="sk_test")


@pytest.fixture
def http_client(settings):
    return RapydHttpClient(settings)


def success_response(data=None):
    """Build a Rapyd success envelope."""
    return {
        "status": {
            "error_code": "",
            "status": "SUCCESS",
            "message": "",
            "response_code": "",
            "operation_id": "op_test",
        },
        "data": data or {},
    }


def error_response(error_code="GENERAL_ERROR", message="Error", status_code=400):
    return {
        "status": {
            "error_code": error_code,
            "status": "ERROR",
            "message": message,
            "response_code": "",
            "operation_id": "op_err",
        },
        "data": None,
    }
