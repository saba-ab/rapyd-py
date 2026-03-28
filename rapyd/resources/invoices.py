"""Invoices resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payment import Invoice
from rapyd.resources.base import BaseResource


class InvoicesResource(BaseResource):
    """Interact with the Rapyd Invoices API (``/v1/invoices``)."""

    async def create(self, **kwargs: Any) -> Invoice:
        """Create an invoice.

        Args:
            customer: Customer token.
            currency: ISO 4217 currency code.
            description: Invoice description.

        Returns:
            Invoice object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/invoices", body=kwargs)
        return Invoice.model_validate(self._extract_data(resp))

    async def get(self, invoice_id: str) -> Invoice:
        """Retrieve an invoice by ID.

        Args:
            invoice_id: The invoice token.

        Returns:
            Invoice object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/invoices/{invoice_id}")
        return Invoice.model_validate(self._extract_data(resp))

    async def update(self, invoice_id: str, **kwargs: Any) -> Invoice:
        """Update an invoice.

        Args:
            invoice_id: The invoice token.
            description: Updated description.
            metadata: Updated metadata.

        Returns:
            Updated Invoice object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/invoices/{invoice_id}", body=kwargs)
        return Invoice.model_validate(self._extract_data(resp))

    async def delete(self, invoice_id: str) -> dict[str, Any]:
        """Delete an invoice.

        Args:
            invoice_id: The invoice token.

        Returns:
            Deletion confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/invoices/{invoice_id}")
        return self._extract_data(resp)

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Invoice]:
        """List invoices with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Invoice objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/invoices", params=params)
        data = self._extract_data(resp)
        return [Invoice.model_validate(item) for item in (data or [])]

    async def finalize(self, invoice_id: str) -> Invoice:
        """Finalize a draft invoice.

        Args:
            invoice_id: The invoice token.

        Returns:
            Finalized Invoice object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post(f"/v1/invoices/{invoice_id}/finalize")
        return Invoice.model_validate(self._extract_data(resp))

    async def pay(self, invoice_id: str, **kwargs: Any) -> Invoice:
        """Pay an invoice.

        Args:
            invoice_id: The invoice token.
            payment_method: Payment method to use.

        Returns:
            Paid Invoice object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post(f"/v1/invoices/{invoice_id}/pay", body=kwargs or None)
        return Invoice.model_validate(self._extract_data(resp))
