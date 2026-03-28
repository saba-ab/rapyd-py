"""Virtual Accounts resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.wallet import VirtualAccount
from rapyd.resources.base import BaseResource


class VirtualAccountsResource(BaseResource):
    """Interact with the Rapyd Virtual Accounts API (``/v1/virtual_accounts``)."""

    async def create(self, **kwargs: Any) -> VirtualAccount:
        """Issue a virtual account (IBAN).

        Args:
            currency: ISO 4217 currency code.
            country: ISO 3166-1 alpha-2 country code.
            ewallet: eWallet token to associate.
            description: Account description.

        Returns:
            VirtualAccount object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/virtual_accounts", body=kwargs)
        return VirtualAccount.model_validate(self._extract_data(resp))

    async def get(self, va_id: str) -> VirtualAccount:
        """Retrieve a virtual account by ID.

        Args:
            va_id: The virtual account token.

        Returns:
            VirtualAccount object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/virtual_accounts/{va_id}")
        return VirtualAccount.model_validate(self._extract_data(resp))

    async def update(self, va_id: str, **kwargs: Any) -> VirtualAccount:
        """Update a virtual account.

        Args:
            va_id: The virtual account token.
            description: Updated description.

        Returns:
            Updated VirtualAccount object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/virtual_accounts/{va_id}", body=kwargs)
        return VirtualAccount.model_validate(self._extract_data(resp))

    async def close(self, va_id: str) -> dict[str, Any]:
        """Close a virtual account.

        Args:
            va_id: The virtual account token.

        Returns:
            Closure confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/virtual_accounts/{va_id}")
        return self._extract_data(resp)

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[VirtualAccount]:
        """List virtual accounts with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of VirtualAccount objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/virtual_accounts", params=params)
        data = self._extract_data(resp)
        return [VirtualAccount.model_validate(item) for item in (data or [])]
