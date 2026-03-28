"""Refunds resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payment import Refund
from rapyd.resources.base import BaseResource


class RefundsResource(BaseResource):
    """Interact with the Rapyd Refunds API (``/v1/refunds``)."""

    async def create(self, **kwargs: Any) -> Refund:
        """Create a refund.

        Args:
            payment: Payment token to refund.
            amount: Refund amount (optional — defaults to full).
            currency: ISO 4217 currency code.
            reason: Reason for the refund.
            metadata: Arbitrary key-value metadata.

        Returns:
            Refund object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/refunds", body=kwargs)
        return Refund.model_validate(self._extract_data(resp))

    async def get(self, refund_id: str) -> Refund:
        """Retrieve a refund by ID.

        Args:
            refund_id: The refund token.

        Returns:
            Refund object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/refunds/{refund_id}")
        return Refund.model_validate(self._extract_data(resp))

    async def update(self, refund_id: str, **kwargs: Any) -> Refund:
        """Update a refund.

        Args:
            refund_id: The refund token.
            metadata: Updated metadata.

        Returns:
            Updated Refund object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/refunds/{refund_id}", body=kwargs)
        return Refund.model_validate(self._extract_data(resp))

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Refund]:
        """List refunds with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Refund objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/refunds", params=params)
        data = self._extract_data(resp)
        return [Refund.model_validate(item) for item in (data or [])]

    async def list_by_payment(self, payment_id: str) -> list[Refund]:
        """List all refunds for a specific payment.

        Args:
            payment_id: The payment token.

        Returns:
            List of Refund objects.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/payments/{payment_id}/refunds")
        data = self._extract_data(resp)
        return [Refund.model_validate(item) for item in (data or [])]
