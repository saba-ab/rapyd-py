"""Data / Utilities resource."""

from __future__ import annotations

from typing import Any

from rapyd.resources.base import BaseResource


class DataResource(BaseResource):
    """Interact with the Rapyd Data & Utilities API (countries, currencies, FX)."""

    async def countries(self) -> list[dict[str, Any]]:
        """List all supported countries.

        Returns:
            List of country dicts.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get("/v1/data/countries")
        return self._extract_data(resp) or []

    async def currencies(self) -> list[dict[str, Any]]:
        """List all supported currencies.

        Returns:
            List of currency dicts.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get("/v1/data/currencies")
        return self._extract_data(resp) or []

    async def fx_rate(self, **kwargs: Any) -> dict[str, Any]:
        """Get an FX rate.

        Args:
            buy_currency: Currency to buy.
            sell_currency: Currency to sell.
            amount: Amount for the conversion.
            fixed_side: "buy" or "sell".

        Returns:
            Dict with FX rate details.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get("/v1/rates/fxrate", params=kwargs)
        return self._extract_data(resp) or {}

    async def daily_rate(self, **kwargs: Any) -> dict[str, Any]:
        """Get the daily FX rate.

        Args:
            buy_currency: Currency to buy.
            sell_currency: Currency to sell.
            amount: Amount for the conversion.
            fixed_side: "buy" or "sell".

        Returns:
            Dict with daily rate details.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get("/v1/rates/daily", params=kwargs)
        return self._extract_data(resp) or {}
