"""Wallet Contacts resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.wallet import WalletContact
from rapyd.resources.base import BaseResource


class WalletContactsResource(BaseResource):
    """Interact with the Rapyd Wallet Contacts API."""

    async def create(self, wallet_id: str, **kwargs: Any) -> WalletContact:
        """Add a contact to a wallet.

        Args:
            wallet_id: The eWallet token.
            first_name: Contact first name.
            last_name: Contact last name.
            email: Contact email.
            contact_type: "personal" or "business".

        Returns:
            WalletContact object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post(f"/v1/user/{wallet_id}/contacts", body=kwargs)
        return WalletContact.model_validate(self._extract_data(resp))

    async def get(self, wallet_id: str, contact_id: str) -> WalletContact:
        """Retrieve a contact from a wallet.

        Args:
            wallet_id: The eWallet token.
            contact_id: The contact token.

        Returns:
            WalletContact object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/user/{wallet_id}/contacts/{contact_id}")
        return WalletContact.model_validate(self._extract_data(resp))

    async def update(self, wallet_id: str, contact_id: str, **kwargs: Any) -> WalletContact:
        """Update a wallet contact.

        Args:
            wallet_id: The eWallet token.
            contact_id: The contact token.

        Returns:
            Updated WalletContact object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/user/{wallet_id}/contacts/{contact_id}", body=kwargs)
        return WalletContact.model_validate(self._extract_data(resp))

    async def delete(self, wallet_id: str, contact_id: str) -> dict[str, Any]:
        """Delete a wallet contact.

        Args:
            wallet_id: The eWallet token.
            contact_id: The contact token.

        Returns:
            Deletion confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/user/{wallet_id}/contacts/{contact_id}")
        return self._extract_data(resp)

    async def list(
        self,
        wallet_id: str,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[WalletContact]:
        """List contacts for a wallet.

        Args:
            wallet_id: The eWallet token.
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of WalletContact objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get(f"/v1/user/{wallet_id}/contacts", params=params)
        data = self._extract_data(resp)
        return [WalletContact.model_validate(item) for item in (data or [])]
