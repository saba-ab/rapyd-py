"""Card Programs resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.issuing import CardProgram
from rapyd.resources.base import BaseResource


class CardProgramsResource(BaseResource):
    """Interact with the Rapyd Card Programs API (``/v1/issuing/card_programs``)."""

    async def create(self, **kwargs: Any) -> CardProgram:
        """Create a card program.

        Args:
            name: Program name.
            card_type: Card type.
            card_brand: Card brand.
            country: ISO 3166-1 alpha-2 country code.
            currency: ISO 4217 currency code.

        Returns:
            CardProgram object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/issuing/card_programs", body=kwargs)
        return CardProgram.model_validate(self._extract_data(resp))

    async def get(self, program_id: str) -> CardProgram:
        """Retrieve a card program by ID.

        Args:
            program_id: The card program token.

        Returns:
            CardProgram object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/issuing/card_programs/{program_id}")
        return CardProgram.model_validate(self._extract_data(resp))

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[CardProgram]:
        """List card programs with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of CardProgram objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/issuing/card_programs", params=params)
        data = self._extract_data(resp)
        return [CardProgram.model_validate(item) for item in (data or [])]
