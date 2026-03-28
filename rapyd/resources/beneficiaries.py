"""Beneficiaries resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payout import Beneficiary
from rapyd.resources.base import BaseResource


class BeneficiariesResource(BaseResource):
    """Interact with the Rapyd Beneficiaries API (``/v1/payouts/beneficiary``)."""

    async def create(self, **kwargs: Any) -> Beneficiary:
        """Create a beneficiary.

        Args:
            category: Payout method category (bank, cash, card, ewallet).
            country: ISO 3166-1 alpha-2 country code.
            currency: ISO 4217 currency code.
            entity_type: "individual" or "company".
            first_name: Beneficiary first name.
            last_name: Beneficiary last name.

        Returns:
            Beneficiary object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/payouts/beneficiary", body=kwargs)
        return Beneficiary.model_validate(self._extract_data(resp))

    async def get(self, beneficiary_id: str) -> Beneficiary:
        """Retrieve a beneficiary by ID.

        Args:
            beneficiary_id: The beneficiary token.

        Returns:
            Beneficiary object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/payouts/beneficiary/{beneficiary_id}")
        return Beneficiary.model_validate(self._extract_data(resp))

    async def update(self, beneficiary_id: str, **kwargs: Any) -> Beneficiary:
        """Update a beneficiary.

        Args:
            beneficiary_id: The beneficiary token.

        Returns:
            Updated Beneficiary object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/payouts/beneficiary/{beneficiary_id}", body=kwargs)
        return Beneficiary.model_validate(self._extract_data(resp))

    async def delete(self, beneficiary_id: str) -> dict[str, Any]:
        """Delete a beneficiary.

        Args:
            beneficiary_id: The beneficiary token.

        Returns:
            Deletion confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/payouts/beneficiary/{beneficiary_id}")
        return self._extract_data(resp)

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Beneficiary]:
        """List beneficiaries with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Beneficiary objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/payouts/beneficiary", params=params)
        data = self._extract_data(resp)
        return [Beneficiary.model_validate(item) for item in (data or [])]
