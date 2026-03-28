"""Customers resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payment import Customer
from rapyd.resources.base import BaseResource


class CustomersResource(BaseResource):
    """Interact with the Rapyd Customers API (``/v1/customers``)."""

    async def create(self, **kwargs: Any) -> Customer:
        """Create a customer.

        Args:
            name: Customer full name.
            email: Customer email address.
            phone_number: Customer phone number.
            payment_method: Default payment method object.
            metadata: Arbitrary key-value metadata.

        Returns:
            Customer object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/customers", body=kwargs)
        return Customer.model_validate(self._extract_data(resp))

    async def get(self, customer_id: str) -> Customer:
        """Retrieve a customer by ID.

        Args:
            customer_id: The customer token (e.g. "cus_xxx").

        Returns:
            Customer object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/customers/{customer_id}")
        return Customer.model_validate(self._extract_data(resp))

    async def update(self, customer_id: str, **kwargs: Any) -> Customer:
        """Update a customer.

        Args:
            customer_id: The customer token.
            name: Updated name.
            email: Updated email.
            metadata: Updated metadata.

        Returns:
            Updated Customer object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/customers/{customer_id}", body=kwargs)
        return Customer.model_validate(self._extract_data(resp))

    async def delete(self, customer_id: str) -> dict[str, Any]:
        """Delete a customer.

        Args:
            customer_id: The customer token.

        Returns:
            Deletion confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/customers/{customer_id}")
        return self._extract_data(resp)

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Customer]:
        """List customers with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Customer objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/customers", params=params)
        data = self._extract_data(resp)
        return [Customer.model_validate(item) for item in (data or [])]

    async def add_payment_method(self, customer_id: str, **kwargs: Any) -> dict[str, Any]:
        """Add a payment method to a customer.

        Args:
            customer_id: The customer token.
            type: Payment method type string.
            fields: Payment method fields dict.

        Returns:
            Payment method data dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post(f"/v1/customers/{customer_id}/payment_methods", body=kwargs)
        return self._extract_data(resp)

    async def list_payment_methods(self, customer_id: str) -> list[dict[str, Any]]:
        """List payment methods for a customer.

        Args:
            customer_id: The customer token.

        Returns:
            List of payment method dicts.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/customers/{customer_id}/payment_methods")
        return self._extract_data(resp) or []

    async def delete_payment_method(self, customer_id: str, pm_id: str) -> dict[str, Any]:
        """Delete a payment method from a customer.

        Args:
            customer_id: The customer token.
            pm_id: The payment method token.

        Returns:
            Deletion confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/customers/{customer_id}/payment_methods/{pm_id}")
        return self._extract_data(resp)
