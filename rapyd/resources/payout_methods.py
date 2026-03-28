"""Payout Methods resource."""

from __future__ import annotations

from typing import Any

from rapyd.resources.base import BaseResource


class PayoutMethodsResource(BaseResource):
    """Interact with the Rapyd Payout Methods API."""

    async def list(
        self,
        country: str | None = None,
        currency: str | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """List available payout method types.

        Args:
            country: Filter by beneficiary country.
            currency: Filter by payout currency.

        Returns:
            List of payout method type dicts.

        Rapyd docs: https://docs.rapyd.net
        """
        params: dict[str, Any] = {**kwargs}
        if country:
            params["beneficiary_country"] = country
        if currency:
            params["payout_currency"] = currency
        resp = await self._get("/v1/payout_method_types", params=params or None)
        return self._extract_data(resp) or []

    async def list_types(self, payout_id: str) -> list[dict[str, Any]]:
        """List payout method types for a specific payout.

        Args:
            payout_id: The payout token.

        Returns:
            List of payout method type dicts.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/payouts/{payout_id}/payout_method_types")
        return self._extract_data(resp) or []

    async def required_fields(self, payout_method_type: str) -> dict[str, Any]:
        """Get required fields for a payout method type.

        Args:
            payout_method_type: The payout method type string.

        Returns:
            Dict describing required fields.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/payouts/required_fields/{payout_method_type}")
        return self._extract_data(resp) or {}
