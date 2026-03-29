"""Wallet Transactions resource."""

from __future__ import annotations

from rapyd.models.wallet import WalletTransaction
from rapyd.resources.base import BaseResource


class WalletTransactionsResource(BaseResource):
    """Interact with the Rapyd Wallet Transactions API."""

    async def list(
        self,
        wallet_id: str,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[WalletTransaction]:
        """List transactions for a wallet.

        Args:
            wallet_id: The eWallet token.
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of WalletTransaction objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get(f"/v1/user/{wallet_id}/transactions", params=params)
        data = self._extract_data(resp)
        return [WalletTransaction.model_validate(item) for item in (data or [])]

    async def get(self, wallet_id: str, transaction_id: str) -> WalletTransaction:
        """Retrieve a specific wallet transaction.

        Args:
            wallet_id: The eWallet token.
            transaction_id: The transaction token.

        Returns:
            WalletTransaction object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/user/{wallet_id}/transactions/{transaction_id}")
        return WalletTransaction.model_validate(self._extract_data(resp))
