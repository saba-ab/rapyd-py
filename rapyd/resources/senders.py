"""Senders resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payout import Sender
from rapyd.resources.base import BaseResource


class SendersResource(BaseResource):
    """Interact with the Rapyd Senders API (``/v1/payouts/sender``)."""

    async def create(self, **kwargs: Any) -> Sender:
        """Create a sender.

        Args:
            country: ISO 3166-1 alpha-2 country code.
            currency: ISO 4217 currency code.
            entity_type: "individual" or "company".
            company_name: Sender company name (if company).
            first_name: Sender first name (if individual).
            last_name: Sender last name (if individual).

        Returns:
            Sender object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/payouts/sender", body=kwargs)
        return Sender.model_validate(self._extract_data(resp))

    async def get(self, sender_id: str) -> Sender:
        """Retrieve a sender by ID.

        Args:
            sender_id: The sender token.

        Returns:
            Sender object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/payouts/sender/{sender_id}")
        return Sender.model_validate(self._extract_data(resp))

    async def update(self, sender_id: str, **kwargs: Any) -> Sender:
        """Update a sender.

        Args:
            sender_id: The sender token.

        Returns:
            Updated Sender object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/payouts/sender/{sender_id}", body=kwargs)
        return Sender.model_validate(self._extract_data(resp))

    async def delete(self, sender_id: str) -> dict[str, Any]:
        """Delete a sender.

        Args:
            sender_id: The sender token.

        Returns:
            Deletion confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/payouts/sender/{sender_id}")
        return self._extract_data(resp)

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Sender]:
        """List senders with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Sender objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/payouts/sender", params=params)
        data = self._extract_data(resp)
        return [Sender.model_validate(item) for item in (data or [])]
