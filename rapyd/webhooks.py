"""Webhook signature verification, event parsing, and handler dispatch."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from rapyd.auth import verify_webhook_signature
from rapyd.exceptions import RapydWebhookError
from rapyd.models.issuing import Card, CardTransaction
from rapyd.models.payment import (
    Customer,
    Dispute,
    Invoice,
    Payment,
    Refund,
    Subscription,
)
from rapyd.models.payout import Payout
from rapyd.models.wallet import VirtualAccount, Wallet, WalletTransaction, WalletTransfer
from rapyd.models.webhook import WebhookEvent

# Map webhook type strings to the Pydantic model for the event data.
# Types not in this map will have their data left as a raw dict.
WEBHOOK_TYPE_MAP: dict[str, type[Any]] = {
    # Payment
    "PAYMENT_COMPLETED": Payment,
    "PAYMENT_SUCCEEDED": Payment,
    "PAYMENT_FAILED": Payment,
    "PAYMENT_EXPIRED": Payment,
    "PAYMENT_UPDATED": Payment,
    "PAYMENT_CAPTURED": Payment,
    "PAYMENT_CANCELED": Payment,
    "PAYMENT_REFUND_COMPLETED": Refund,
    "PAYMENT_REFUND_FAILED": Refund,
    "PAYMENT_REFUND_REJECTED": Refund,
    "PAYMENT_DISPUTE_CREATED": Dispute,
    "PAYMENT_DISPUTE_UPDATED": Dispute,
    # Refund
    "REFUND_COMPLETED": Refund,
    "REFUND_FAILED": Refund,
    "REFUND_REJECTED": Refund,
    # Customer
    "CUSTOMER_CREATED": Customer,
    "CUSTOMER_UPDATED": Customer,
    "CUSTOMER_DELETED": Customer,
    "CUSTOMER_PAYMENT_METHOD_CREATED": Customer,
    "CUSTOMER_PAYMENT_METHOD_UPDATED": Customer,
    "CUSTOMER_PAYMENT_METHOD_DELETED": Customer,
    "CUSTOMER_PAYMENT_METHOD_EXPIRING": Customer,
    # Subscription
    "CUSTOMER_SUBSCRIPTION_CREATED": Subscription,
    "CUSTOMER_SUBSCRIPTION_UPDATED": Subscription,
    "CUSTOMER_SUBSCRIPTION_COMPLETED": Subscription,
    "CUSTOMER_SUBSCRIPTION_CANCELED": Subscription,
    "CUSTOMER_SUBSCRIPTION_PAST_DUE": Subscription,
    "CUSTOMER_SUBSCRIPTION_TRIAL_END": Subscription,
    "CUSTOMER_SUBSCRIPTION_RENEWED": Subscription,
    # Invoice
    "INVOICE_CREATED": Invoice,
    "INVOICE_UPDATED": Invoice,
    "INVOICE_PAYMENT_CREATED": Invoice,
    "INVOICE_PAYMENT_SUCCEEDED": Invoice,
    "INVOICE_PAYMENT_FAILED": Invoice,
    # Payout
    "PAYOUT_COMPLETED": Payout,
    "PAYOUT_UPDATED": Payout,
    "PAYOUT_FAILED": Payout,
    "PAYOUT_EXPIRED": Payout,
    "PAYOUT_CANCELED": Payout,
    "PAYOUT_RETURNED": Payout,
    # Wallet
    "WALLET_TRANSACTION": WalletTransaction,
    "WALLET_FUNDS_ADDED": Wallet,
    "WALLET_FUNDS_REMOVED": Wallet,
    "WALLET_TRANSFER_COMPLETED": WalletTransfer,
    "WALLET_TRANSFER_FAILED": WalletTransfer,
    "WALLET_TRANSFER_RESPONSE_RECEIVED": WalletTransfer,
    # Card Issuing
    "CARD_ISSUING_AUTHORIZATION_APPROVED": CardTransaction,
    "CARD_ISSUING_AUTHORIZATION_DECLINED": CardTransaction,
    "CARD_ISSUING_SALE": CardTransaction,
    "CARD_ISSUING_CREDIT": CardTransaction,
    "CARD_ISSUING_REVERSAL": CardTransaction,
    "CARD_ISSUING_REFUND": CardTransaction,
    "CARD_ISSUING_CHARGEBACK": CardTransaction,
    "CARD_ISSUING_ADJUSTMENT": CardTransaction,
    "CARD_ISSUING_ATM_FEE": CardTransaction,
    "CARD_ISSUING_ATM_WITHDRAWAL": CardTransaction,
    "CARD_ADDED_SUCCESSFULLY": Card,
    "CARD_ISSUING_TRANSACTION_COMPLETED": CardTransaction,
    # Verify
    "VERIFY_APPLICATION_SUBMITTED": dict,
    "VERIFY_APPLICATION_APPROVED": dict,
    "VERIFY_APPLICATION_REJECTED": dict,
    # Virtual Accounts
    "VIRTUAL_ACCOUNT_CREATED": VirtualAccount,
    "VIRTUAL_ACCOUNT_UPDATED": VirtualAccount,
    "VIRTUAL_ACCOUNT_CLOSED": VirtualAccount,
    "VIRTUAL_ACCOUNT_TRANSACTION": VirtualAccount,
}


def parse_webhook_event(
    payload: str | bytes,
    *,
    salt: str,
    timestamp: str,
    signature: str,
    access_key: str,
    secret_key: str,
    webhook_url: str,
) -> WebhookEvent[Any]:
    """Verify a webhook signature and parse the event.

    Args:
        payload: Raw request body (string or bytes).
        salt: ``salt`` header from the webhook request.
        timestamp: ``timestamp`` header from the webhook request.
        signature: ``signature`` header from the webhook request.
        access_key: Your Rapyd access key.
        secret_key: Your Rapyd secret key.
        webhook_url: The full webhook URL configured in the Rapyd Client Portal.

    Returns:
        A typed WebhookEvent with the parsed data model.

    Raises:
        RapydWebhookError: If the signature is invalid.
    """
    body_string = payload if isinstance(payload, str) else payload.decode("utf-8")

    if not verify_webhook_signature(
        url_path=webhook_url,
        salt=salt,
        timestamp=timestamp,
        signature=signature,
        access_key=access_key,
        secret_key=secret_key,
        body_string=body_string,
    ):
        raise RapydWebhookError("Invalid webhook signature")

    raw = json.loads(body_string)
    event_type = raw.get("type", "")

    # Deserialise the data payload into the appropriate model
    model_cls = WEBHOOK_TYPE_MAP.get(event_type)
    data_raw = raw.get("data", {})
    if model_cls and model_cls is not dict:
        data = model_cls.model_validate(data_raw)
    else:
        data = data_raw

    return WebhookEvent(
        id=raw.get("id", ""),
        type=event_type,
        data=data,
        trigger_operation_id=raw.get("trigger_operation_id", ""),
        status=raw.get("status", ""),
        created_at=raw.get("created_at", 0),
    )


class WebhookHandler:
    """OOP-style webhook event dispatcher.

    Usage::

        handler = WebhookHandler()

        @handler.on("PAYMENT_COMPLETED")
        async def on_payment(event: WebhookEvent):
            print(event.data.id)

        await handler.dispatch(event)
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[..., Any]]] = {}

    def on(self, event_type: str, handler: Callable[..., Any] | None = None) -> Any:
        """Register a handler for a webhook event type.

        Can be used as a decorator or called directly.

        Args:
            event_type: Webhook event type string (e.g. "PAYMENT_COMPLETED").
            handler: Handler callable (optional if used as decorator).

        Returns:
            The handler function (when used as decorator).
        """
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            self._handlers.setdefault(event_type, []).append(fn)
            return fn

        if handler is not None:
            decorator(handler)
            return handler
        return decorator

    async def dispatch(self, event: WebhookEvent[Any]) -> None:
        """Dispatch a webhook event to registered handlers.

        Args:
            event: The parsed WebhookEvent.
        """
        for handler in self._handlers.get(event.type, []):
            result = handler(event)
            # Support both sync and async handlers
            if hasattr(result, "__await__"):
                await result
