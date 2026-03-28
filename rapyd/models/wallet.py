"""Pydantic models for Wallet domain."""

from __future__ import annotations

from typing import Any

from rapyd.models.base import RapydObject


class WalletAccount(RapydObject):
    """Account within a Rapyd Wallet (one per currency)."""

    currency: str = ""
    alias: str = ""
    balance: float = 0.0
    received_balance: float = 0.0
    on_hold_balance: float = 0.0
    reserve_balance: float = 0.0


class Wallet(RapydObject):
    """Rapyd eWallet object."""

    phone_number: str = ""
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    status: str = ""
    type: str = ""
    ewallet_reference_id: str = ""
    metadata: dict[str, Any] | None = None
    accounts: list[WalletAccount] | None = None
    category: str | None = None
    contacts: dict[str, Any] | None = None
    created_at: int = 0
    updated_at: int = 0


class WalletContact(RapydObject):
    """Contact on a Rapyd eWallet."""

    first_name: str = ""
    last_name: str = ""
    middle_name: str = ""
    email: str = ""
    phone_number: str = ""
    contact_type: str = ""
    date_of_birth: str = ""
    country: str = ""
    nationality: str = ""
    gender: str = ""
    address: dict[str, Any] | None = None
    identification_type: str = ""
    identification_number: str = ""
    ewallet: str = ""
    metadata: dict[str, Any] | None = None
    created_at: int = 0
    business_details: dict[str, Any] | None = None


class WalletTransaction(RapydObject):
    """Rapyd Wallet Transaction object."""

    amount: float = 0.0
    currency: str = ""
    balance_type: str = ""
    type: str = ""
    status: str = ""
    reason: str = ""
    ewallet_id: str = ""
    balance: float = 0.0
    metadata: dict[str, Any] | None = None
    created_at: int = 0


class WalletTransfer(RapydObject):
    """Rapyd Wallet Transfer object."""

    source_ewallet: str = ""
    destination_ewallet: str = ""
    amount: float = 0.0
    currency: str = ""
    status: str = ""
    response_metadata: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    created_at: int = 0


class VirtualAccount(RapydObject):
    """Rapyd Virtual Account (IBAN) object."""

    currency: str = ""
    country_iso: str = ""
    status: str = ""
    description: str = ""
    ewallet: str = ""
    merchant_reference_id: str = ""
    bank_account: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    transactions: list[dict[str, Any]] | None = None
    requested_currency: str = ""
    created_at: int = 0
    updated_at: int = 0
