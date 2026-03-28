"""Tests for RapydClient."""

from unittest.mock import AsyncMock, patch

from rapyd.client import RapydClient
from rapyd.resources.payments import PaymentsResource
from rapyd.resources.wallets import WalletsResource
from rapyd.resources.payouts import PayoutsResource


def test_client_init_from_env(monkeypatch):
    monkeypatch.setenv("RAPYD_ACCESS_KEY", "ak_env")
    monkeypatch.setenv("RAPYD_SECRET_KEY", "sk_env")
    client = RapydClient()
    assert client._settings.rapyd_access_key == "ak_env"
    assert client._settings.rapyd_environment == "sandbox"


def test_client_init_from_args():
    client = RapydClient(access_key="ak_args", secret_key="sk_args", environment="production")
    assert client._settings.rapyd_access_key == "ak_args"
    assert client._settings.rapyd_environment == "production"
    assert client._settings.base_url == "https://api.rapyd.net"


def test_resource_accessors_return_correct_types():
    client = RapydClient(access_key="ak", secret_key="sk")
    assert isinstance(client.payments(), PaymentsResource)
    assert isinstance(client.wallets(), WalletsResource)
    assert isinstance(client.payouts(), PayoutsResource)


def test_resource_accessors_are_cached():
    client = RapydClient(access_key="ak", secret_key="sk")
    p1 = client.payments()
    p2 = client.payments()
    assert p1 is p2

    w1 = client.wallets()
    w2 = client.wallets()
    assert w1 is w2


async def test_async_context_manager_calls_aclose():
    client = RapydClient(access_key="ak", secret_key="sk")
    client._http.aclose = AsyncMock()

    async with client:
        pass

    client._http.aclose.assert_awaited_once()
