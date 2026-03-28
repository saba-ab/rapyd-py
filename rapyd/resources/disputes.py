"""Disputes resource."""

from __future__ import annotations

from typing import Any

from rapyd.resources.base import BaseResource


class DisputesResource(BaseResource):
    """Interact with the Rapyd Disputes API (``/v1/payment_disputes``)."""

    async def get(self, dispute_id: str) -> dict[str, Any]:
        """Retrieve a dispute by ID.

        Args:
            dispute_id: The dispute token.

        Returns:
            Dispute data dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/payment_disputes/{dispute_id}")
        return self._extract_data(resp)

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[dict[str, Any]]:
        """List disputes with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of dispute dicts.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/payment_disputes", params=params)
        return self._extract_data(resp) or []
