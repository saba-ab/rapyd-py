"""rapyd-sdk — Async Python SDK for the Rapyd Fintech-as-a-Service API."""

from rapyd.client import RapydClient
from rapyd.enums import (
    CardBlockReasonCode,
    CardStatus,
    CheckoutPageStatus,
    CouponDuration,
    DisputeStatus,
    EntityType,
    Environment,
    EscrowStatus,
    FeeCalcType,
    FixedSide,
    InvoiceStatus,
    IssuingTxnType,
    NextAction,
    PaymentFlowType,
    PaymentMethodCategory,
    PaymentStatus,
    PayoutMethodCategory,
    PayoutStatus,
    PlanInterval,
    RefundStatus,
    SubscriptionStatus,
    WalletContactType,
    WebhookEventType,
    WebhookStatus,
)
from rapyd.exceptions import (
    RapydApiError,
    RapydAuthError,
    RapydConnectionError,
    RapydException,
    RapydTimeoutError,
    RapydValidationError,
    RapydWebhookError,
)
from rapyd.pagination import paginate
from rapyd.webhooks import WebhookHandler, parse_webhook_event

__version__ = "1.0.0"

__all__ = [
    # Client
    "RapydClient",
    # Exceptions
    "RapydException",
    "RapydApiError",
    "RapydAuthError",
    "RapydValidationError",
    "RapydWebhookError",
    "RapydTimeoutError",
    "RapydConnectionError",
    # Webhooks
    "parse_webhook_event",
    "WebhookHandler",
    # Pagination
    "paginate",
    # Enums
    "PaymentStatus",
    "PaymentMethodCategory",
    "PaymentFlowType",
    "NextAction",
    "RefundStatus",
    "DisputeStatus",
    "PayoutStatus",
    "PayoutMethodCategory",
    "SubscriptionStatus",
    "InvoiceStatus",
    "WebhookStatus",
    "CardStatus",
    "CardBlockReasonCode",
    "EntityType",
    "FeeCalcType",
    "FixedSide",
    "WalletContactType",
    "CouponDuration",
    "PlanInterval",
    "CheckoutPageStatus",
    "EscrowStatus",
    "IssuingTxnType",
    "Environment",
    "WebhookEventType",
]
