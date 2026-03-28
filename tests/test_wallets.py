"""Tests for Wallet resources."""

from pytest_httpx import HTTPXMock

from rapyd.models.wallet import Wallet, WalletContact, WalletTransfer
from rapyd.resources.wallet_contacts import WalletContactsResource
from rapyd.resources.wallet_transfers import WalletTransfersResource
from rapyd.resources.wallets import WalletsResource
from tests.conftest import success_response


async def test_create_wallet(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "ewallet_123",
        "first_name": "John",
        "last_name": "Doe",
        "status": "ACT",
    }))

    resource = WalletsResource(http_client)
    wallet = await resource.create(first_name="John", last_name="Doe")

    assert isinstance(wallet, Wallet)
    assert wallet.id == "ewallet_123"
    assert wallet.first_name == "John"


async def test_wallet_contact_create(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "cont_123",
        "first_name": "Jane",
        "contact_type": "personal",
        "ewallet": "ewallet_123",
    }))

    resource = WalletContactsResource(http_client)
    contact = await resource.create("ewallet_123", first_name="Jane", contact_type="personal")

    assert isinstance(contact, WalletContact)
    assert contact.id == "cont_123"
    assert contact.ewallet == "ewallet_123"


async def test_wallet_transfer_create(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response({
        "id": "wt_123",
        "source_ewallet": "ewallet_src",
        "destination_ewallet": "ewallet_dst",
        "amount": 100.0,
        "currency": "USD",
        "status": "PEN",
    }))

    resource = WalletTransfersResource(http_client)
    transfer = await resource.create(
        source_ewallet="ewallet_src",
        destination_ewallet="ewallet_dst",
        amount=100.0,
        currency="USD",
    )

    assert isinstance(transfer, WalletTransfer)
    assert transfer.id == "wt_123"
    assert transfer.amount == 100.0


async def test_list_wallets(httpx_mock: HTTPXMock, http_client):
    httpx_mock.add_response(json=success_response([
        {"id": "ewallet_1"},
        {"id": "ewallet_2"},
    ]))

    resource = WalletsResource(http_client)
    wallets = await resource.list(limit=10)

    assert len(wallets) == 2
    assert all(isinstance(w, Wallet) for w in wallets)
