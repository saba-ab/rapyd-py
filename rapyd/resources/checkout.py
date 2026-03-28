"""Checkout resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payment import Checkout
from rapyd.resources.base import BaseResource


class CheckoutResource(BaseResource):
    """Interact with the Rapyd Checkout API (``/v1/checkout``)."""

    async def create(self, **kwargs: Any) -> Checkout:
        """Create a checkout page.

        Args:
            amount: Checkout amount.
            country: ISO 3166-1 alpha-2 country code.
            currency: ISO 4217 currency code.
            complete_checkout_url: URL to redirect on success.
            error_payment_url: URL to redirect on error.
            payment_method_types_include: List of allowed payment method types.

        Returns:
            Checkout object with redirect_url.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/checkout", body=kwargs)
        return Checkout.model_validate(self._extract_data(resp))

    async def get(self, checkout_id: str) -> Checkout:
        """Retrieve a checkout page by ID.

        Args:
            checkout_id: The checkout token.

        Returns:
            Checkout object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/checkout/{checkout_id}")
        return Checkout.model_validate(self._extract_data(resp))
