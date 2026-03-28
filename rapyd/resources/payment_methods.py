"""Payment Methods resource."""

from __future__ import annotations

from typing import Any

from rapyd.resources.base import BaseResource


class PaymentMethodsResource(BaseResource):
    """Interact with the Rapyd Payment Methods API."""

    async def list_by_country(self, country: str) -> list[dict[str, Any]]:
        """List available payment methods for a country.

        Args:
            country: ISO 3166-1 alpha-2 country code (e.g. "US").

        Returns:
            List of payment method type dicts.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get("/v1/payment_methods/country", params={"country": country})
        return self._extract_data(resp) or []

    async def required_fields(self, payment_method_type: str) -> dict[str, Any]:
        """Get required fields for a payment method type.

        Args:
            payment_method_type: The payment method type string (e.g. "us_visa_card").

        Returns:
            Dict describing required fields.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/payment_methods/{payment_method_type}/required_fields")
        return self._extract_data(resp) or {}
