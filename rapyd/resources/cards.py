"""Cards resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.issuing import Card
from rapyd.resources.base import BaseResource


class CardsResource(BaseResource):
    """Interact with the Rapyd Card Issuing API (``/v1/issuing/cards``)."""

    async def create(self, **kwargs: Any) -> Card:
        """Issue a new card.

        Args:
            ewallet_contact: Contact token for the cardholder.
            card_program: Card program token.

        Returns:
            Card object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/issuing/cards", body=kwargs)
        return Card.model_validate(self._extract_data(resp))

    async def get(self, card_id: str) -> Card:
        """Retrieve a card by ID.

        Args:
            card_id: The card token.

        Returns:
            Card object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/issuing/cards/{card_id}")
        return Card.model_validate(self._extract_data(resp))

    async def update(self, card_id: str, **kwargs: Any) -> Card:
        """Update a card.

        Args:
            card_id: The card token.

        Returns:
            Updated Card object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/issuing/cards/{card_id}", body=kwargs)
        return Card.model_validate(self._extract_data(resp))

    async def update_status(self, **kwargs: Any) -> Card:
        """Update a card's status (block/unblock).

        Args:
            card: Card token.
            status: New status (e.g. "BLO", "ACT").
            reason_code: Block reason code.

        Returns:
            Updated Card object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/issuing/cards/status", body=kwargs)
        return Card.model_validate(self._extract_data(resp))

    async def activate(self, **kwargs: Any) -> Card:
        """Activate a card.

        Args:
            card: Card token.

        Returns:
            Activated Card object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/issuing/cards/activate", body=kwargs)
        return Card.model_validate(self._extract_data(resp))

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Card]:
        """List issued cards with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Card objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/issuing/cards", params=params)
        data = self._extract_data(resp)
        return [Card.model_validate(item) for item in (data or [])]

    async def list_transactions(
        self,
        card_id: str,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[dict[str, Any]]:
        """List transactions for a card.

        Args:
            card_id: The card token.
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of card transaction dicts.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get(f"/v1/issuing/cards/{card_id}/transactions", params=params)
        return self._extract_data(resp) or []

    async def set_pin(self, **kwargs: Any) -> dict[str, Any]:
        """Set PIN for a card.

        Args:
            card: Card token.
            pin: 4-digit PIN string.

        Returns:
            Confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/issuing/cards/pin/set", body=kwargs)
        return self._extract_data(resp)

    async def get_pin(self, **kwargs: Any) -> dict[str, Any]:
        """Get PIN for a card.

        Args:
            card: Card token.

        Returns:
            Dict containing the card PIN.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get("/v1/issuing/cards/pin/get", params=kwargs)
        return self._extract_data(resp)
