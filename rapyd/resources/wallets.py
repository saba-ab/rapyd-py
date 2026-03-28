"""Wallets resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.wallet import Wallet
from rapyd.resources.base import BaseResource


class WalletsResource(BaseResource):
    """Interact with the Rapyd Wallets API (``/v1/user``)."""

    async def create(self, **kwargs: Any) -> Wallet:
        """Create an eWallet.

        Args:
            first_name: Wallet owner first name.
            last_name: Wallet owner last name.
            email: Wallet owner email.
            ewallet_reference_id: Your reference ID.
            type: Wallet type.
            contact: Contact object for the wallet.

        Returns:
            Wallet object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/user", body=kwargs)
        return Wallet.model_validate(self._extract_data(resp))

    async def get(self, wallet_id: str) -> Wallet:
        """Retrieve a wallet by ID.

        Args:
            wallet_id: The eWallet token (e.g. "ewallet_xxx").

        Returns:
            Wallet object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/user/{wallet_id}")
        return Wallet.model_validate(self._extract_data(resp))

    async def update(self, wallet_id: str, **kwargs: Any) -> Wallet:
        """Update a wallet.

        Args:
            wallet_id: The eWallet token.
            email: Updated email.
            metadata: Updated metadata.

        Returns:
            Updated Wallet object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/user/{wallet_id}", body=kwargs)
        return Wallet.model_validate(self._extract_data(resp))

    async def delete(self, wallet_id: str) -> dict[str, Any]:
        """Delete a wallet.

        Args:
            wallet_id: The eWallet token.

        Returns:
            Deletion confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/user/{wallet_id}")
        return self._extract_data(resp)

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Wallet]:
        """List wallets with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Wallet objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/user", params=params)
        data = self._extract_data(resp)
        return [Wallet.model_validate(item) for item in (data or [])]
