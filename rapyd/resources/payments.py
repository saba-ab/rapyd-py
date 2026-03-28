"""Payments resource — create, retrieve, update, cancel, list, capture payments."""

from __future__ import annotations

from typing import Any

from rapyd.models.payment import Payment
from rapyd.resources.base import BaseResource


class PaymentsResource(BaseResource):
    """Interact with the Rapyd Payments API (``/v1/payments``)."""

    async def create(self, **kwargs: Any) -> Payment:
        """Create a payment.

        Args:
            amount: Payment amount as a positive float.
            currency: ISO 4217 currency code (e.g. "USD", "GEL").
            payment_method: Payment method object or type string.
            country: ISO 3166-1 alpha-2 country code.
            customer: Customer token for saved payment methods.
            capture: Whether to capture immediately (default True).
            metadata: Arbitrary key-value metadata.

        Returns:
            Payment object with id, status, redirect_url, etc.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/payments", body=kwargs)
        return Payment.model_validate(self._extract_data(resp))

    async def get(self, payment_id: str) -> Payment:
        """Retrieve a payment by ID.

        Args:
            payment_id: The payment token (e.g. "payment_xxx").

        Returns:
            Payment object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/payments/{payment_id}")
        return Payment.model_validate(self._extract_data(resp))

    async def update(self, payment_id: str, **kwargs: Any) -> Payment:
        """Update a payment.

        Args:
            payment_id: The payment token.
            metadata: Updated metadata.
            description: Updated description.

        Returns:
            Updated Payment object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/payments/{payment_id}", body=kwargs)
        return Payment.model_validate(self._extract_data(resp))

    async def cancel(self, payment_id: str) -> Payment:
        """Cancel a payment.

        Args:
            payment_id: The payment token.

        Returns:
            Canceled Payment object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/payments/{payment_id}")
        return Payment.model_validate(self._extract_data(resp))

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Payment]:
        """List payments with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number (1-indexed).
            starting_after: Cursor — ID of object before first result.
            ending_before: Cursor — ID of object after last result.

        Returns:
            List of Payment objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/payments", params=params)
        data = self._extract_data(resp)
        return [Payment.model_validate(item) for item in (data or [])]

    async def capture(self, payment_id: str, **kwargs: Any) -> Payment:
        """Capture an authorized payment.

        Args:
            payment_id: The payment token.
            amount: Amount to capture (optional, defaults to full amount).

        Returns:
            Captured Payment object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post(f"/v1/payments/{payment_id}/capture", body=kwargs or None)
        return Payment.model_validate(self._extract_data(resp))

    async def complete(self, payment_id: str, amount: float) -> Payment:
        """Complete a payment in sandbox.

        Args:
            payment_id: The payment token.
            amount: Amount to complete.

        Returns:
            Completed Payment object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post(f"/v1/payments/completePayment/{payment_id}/{amount}")
        return Payment.model_validate(self._extract_data(resp))
