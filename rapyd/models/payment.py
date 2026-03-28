"""Pydantic models for Collect (Payments) domain."""

from __future__ import annotations

from typing import Any

from rapyd.models.base import RapydAddress, RapydObject


class Payment(RapydObject):
    """Rapyd Payment object."""

    amount: float = 0.0
    original_amount: float = 0.0
    is_partial: bool = False
    currency_code: str = ""
    country_code: str = ""
    status: str = ""
    description: str = ""
    merchant_reference_id: str = ""
    customer_token: str = ""
    payment_method: str | dict[str, Any] | None = None
    payment_method_data: dict[str, Any] | None = None
    payment_method_type: str = ""
    payment_method_type_category: str = ""
    expiration: int = 0
    captured: bool = False
    refunded: bool = False
    refunded_amount: float = 0.0
    receipt_number: str = ""
    flow_type: str = ""
    address: RapydAddress | None = None
    redirect_url: str = ""
    complete_payment_url: str = ""
    error_payment_url: str = ""
    receipt_email: str = ""
    next_action: str = ""
    paid: bool = False
    paid_at: int = 0
    failure_code: str = ""
    failure_message: str = ""
    metadata: dict[str, Any] | None = None
    ewallet_id: str = ""
    ewallets: list[dict[str, Any]] | None = None
    transaction_id: str = ""
    created_at: int = 0
    updated_at: int = 0


class Refund(RapydObject):
    """Rapyd Refund object."""

    payment: str = ""
    amount: float = 0.0
    currency: str = ""
    status: str = ""
    reason: str = ""
    metadata: dict[str, Any] | None = None
    created_at: int = 0
    updated_at: int = 0
    merchant_reference_id: str = ""
    payment_created_at: int = 0
    payment_method_type: str = ""
    ewallets: list[dict[str, Any]] | None = None
    proportional_refund: bool = False


class Customer(RapydObject):
    """Rapyd Customer object."""

    name: str = ""
    email: str = ""
    phone_number: str = ""
    description: str = ""
    addresses: list[RapydAddress] | None = None
    default_payment_method: str = ""
    payment_methods: dict[str, Any] | None = None
    business_vat_id: str = ""
    ewallet: str = ""
    metadata: dict[str, Any] | None = None
    created_at: int = 0


class Checkout(RapydObject):
    """Rapyd Checkout Page object."""

    status: str = ""
    language: str = ""
    page_expiration: int = 0
    redirect_url: str = ""
    complete_checkout_url: str = ""
    error_payment_url: str = ""
    country: str = ""
    currency: str = ""
    amount: float = 0.0
    payment: dict[str, Any] | None = None
    payment_method_types_include: list[str] | None = None
    payment_method_types_exclude: list[str] | None = None
    customer: str = ""
    metadata: dict[str, Any] | None = None
    created_at: int = 0


class PaymentLink(RapydObject):
    """Rapyd Hosted Payment Link object."""

    amount: float = 0.0
    currency: str = ""
    country: str = ""
    status: str = ""
    redirect_url: str = ""
    merchant_reference_id: str = ""
    metadata: dict[str, Any] | None = None
    created_at: int = 0


class Plan(RapydObject):
    """Rapyd subscription Plan object."""

    amount: float = 0.0
    currency: str = ""
    interval: str = ""
    interval_count: int = 1
    product: str | dict[str, Any] | None = None
    billing_scheme: str = ""
    nickname: str = ""
    active: bool = True
    metadata: dict[str, Any] | None = None
    created_at: int = 0
    trial_period_days: int = 0
    usage_type: str = ""
    aggregate_usage: str = ""
    tiers: list[dict[str, Any]] | None = None
    tiers_mode: str = ""
    transform_usage: dict[str, Any] | None = None


class Subscription(RapydObject):
    """Rapyd Subscription object."""

    billing: str = ""
    billing_cycle_anchor: int = 0
    cancel_at_period_end: bool = False
    canceled_at: int = 0
    created_at: int = 0
    current_period_end: int = 0
    current_period_start: int = 0
    customer_token: str = ""
    days_until_due: int = 0
    discount: dict[str, Any] | None = None
    ended_at: int = 0
    metadata: dict[str, Any] | None = None
    payment_fields: dict[str, Any] | None = None
    payment_method: str = ""
    plan: dict[str, Any] | None = None
    quantity: int = 1
    status: str = ""
    subscription_items: list[dict[str, Any]] | None = None
    tax_percent: float = 0.0
    trial_end: int = 0
    trial_start: int = 0
    type: str = ""


class Product(RapydObject):
    """Rapyd Product object."""

    name: str = ""
    type: str = ""
    active: bool = True
    description: str = ""
    metadata: dict[str, Any] | None = None
    images: list[str] | None = None
    shippable: bool | None = None
    statement_descriptor: str = ""
    unit_label: str = ""
    created_at: int = 0
    updated_at: int = 0


class Invoice(RapydObject):
    """Rapyd Invoice object."""

    amount_due: float = 0.0
    amount_paid: float = 0.0
    amount_remaining: float = 0.0
    billing: str = ""
    billing_reason: str = ""
    currency: str = ""
    customer: str = ""
    date: int = 0
    description: str = ""
    discount: dict[str, Any] | None = None
    due_date: int = 0
    lines: list[dict[str, Any]] | None = None
    metadata: dict[str, Any] | None = None
    number: str = ""
    paid: bool = False
    payment: str = ""
    period_end: int = 0
    period_start: int = 0
    status: str = ""
    subscription: str = ""
    subtotal: float = 0.0
    tax: float = 0.0
    tax_percent: float = 0.0
    total: float = 0.0
    created_at: int = 0


class Dispute(RapydObject):
    """Rapyd Payment Dispute object."""

    token: str = ""
    status: str = ""
    amount: float = 0.0
    currency: str = ""
    payment: str = ""
    reason: str = ""
    due_date: int = 0
    metadata: dict[str, Any] | None = None
    created_at: int = 0
    updated_at: int = 0
