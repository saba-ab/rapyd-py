"""Pydantic models for Disburse (Payouts) domain."""

from __future__ import annotations

from typing import Any

from rapyd.models.base import RapydObject


class Payout(RapydObject):
    """Rapyd Payout object."""

    payout_type: str = ""
    payout_amount: float = 0.0
    payout_currency: str = ""
    sender_amount: float = 0.0
    sender_currency: str = ""
    sender_country: str = ""
    status: str = ""
    beneficiary: str | dict[str, Any] | None = None
    sender: str | dict[str, Any] | None = None
    payout_method_type: str = ""
    ewallet: str = ""
    description: str = ""
    merchant_reference_id: str = ""
    metadata: dict[str, Any] | None = None
    fx_rate: float = 0.0
    paid_at: int = 0
    error_code: str = ""
    error_message: str = ""
    created_at: int = 0
    updated_at: int = 0
    confirm_automatically: bool = False
    payout_fees: dict[str, Any] | None = None
    instructions: list[dict[str, Any]] | None = None


class Beneficiary(RapydObject):
    """Rapyd Payout Beneficiary object."""

    category: str = ""
    country: str = ""
    currency: str = ""
    entity_type: str = ""
    first_name: str = ""
    last_name: str = ""
    company_name: str = ""
    identification_type: str = ""
    identification_value: str = ""
    account_number: str = ""
    bank_name: str = ""
    merchant_reference_id: str = ""
    metadata: dict[str, Any] | None = None
    created_at: int = 0


class Sender(RapydObject):
    """Rapyd Payout Sender object."""

    country: str = ""
    currency: str = ""
    entity_type: str = ""
    first_name: str = ""
    last_name: str = ""
    company_name: str = ""
    identification_type: str = ""
    identification_value: str = ""
    merchant_reference_id: str = ""
    metadata: dict[str, Any] | None = None
    created_at: int = 0
