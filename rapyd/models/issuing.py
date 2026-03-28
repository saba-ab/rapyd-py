"""Pydantic models for Issuing (Cards) domain."""

from __future__ import annotations

from typing import Any

from rapyd.models.base import RapydObject


class Card(RapydObject):
    """Rapyd Issued Card object."""

    ewallet_contact: str = ""
    card_program: str = ""
    status: str = ""
    card_number: str = ""
    expiration_month: str = ""
    expiration_year: str = ""
    cvv: str = ""
    pin: str = ""
    bin: str = ""
    last4: str = ""
    card_id: str = ""
    assigned_at: int = 0
    activated_at: int = 0
    blocked_reason: str = ""
    metadata: dict[str, Any] | None = None
    created_at: int = 0
    updated_at: int = 0


class CardProgram(RapydObject):
    """Rapyd Card Program object."""

    name: str = ""
    status: str = ""
    card_type: str = ""
    card_brand: str = ""
    country: str = ""
    currency: str = ""
    spending_limit_local: float | None = None
    spending_limit_global: float | None = None
    metadata: dict[str, Any] | None = None
    created_at: int = 0


class CardTransaction(RapydObject):
    """Rapyd Card Issuing Transaction object."""

    card_id: str = ""
    amount: float = 0.0
    currency: str = ""
    auth_code: str = ""
    merchant_name: str = ""
    merchant_category_code: str = ""
    transaction_type: str = ""
    status: str = ""
    pos_entry_mode: str = ""
    wallet_transaction_id: str = ""
    created_at: int = 0
