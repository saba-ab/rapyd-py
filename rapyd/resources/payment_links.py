"""Payment Links resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payment import PaymentLink
from rapyd.resources.base import BaseResource


class PaymentLinksResource(BaseResource):
    """Interact with the Rapyd Payment Links API (``/v1/hosted/collect/payments``)."""

    async def create(self, **kwargs: Any) -> PaymentLink:
        """Create a hosted payment link.

        Args:
            amount: Payment amount.
            currency: ISO 4217 currency code.
            country: ISO 3166-1 alpha-2 country code.
            merchant_reference_id: Your reference ID.

        Returns:
            PaymentLink object with redirect_url.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/hosted/collect/payments", body=kwargs)
        return PaymentLink.model_validate(self._extract_data(resp))

    async def get(self, link_id: str) -> PaymentLink:
        """Retrieve a payment link by ID.

        Args:
            link_id: The payment link token.

        Returns:
            PaymentLink object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/hosted/collect/payments/{link_id}")
        return PaymentLink.model_validate(self._extract_data(resp))

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[PaymentLink]:
        """List payment links with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of PaymentLink objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/hosted/collect/payments", params=params)
        data = self._extract_data(resp)
        return [PaymentLink.model_validate(item) for item in (data or [])]
