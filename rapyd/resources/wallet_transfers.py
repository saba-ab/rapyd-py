"""Wallet Transfers resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.wallet import WalletTransfer
from rapyd.resources.base import BaseResource


class WalletTransfersResource(BaseResource):
    """Interact with the Rapyd Wallet Transfers API (``/v1/account/transfer``)."""

    async def create(self, **kwargs: Any) -> WalletTransfer:
        """Transfer funds between wallets.

        Args:
            source_ewallet: Source eWallet token.
            destination_ewallet: Destination eWallet token.
            amount: Transfer amount.
            currency: ISO 4217 currency code.

        Returns:
            WalletTransfer object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/account/transfer", body=kwargs)
        return WalletTransfer.model_validate(self._extract_data(resp))

    async def set_response(self, **kwargs: Any) -> WalletTransfer:
        """Set the response on a wallet transfer (accept/decline).

        Args:
            id: Transfer token.
            status: "accept" or "decline".

        Returns:
            Updated WalletTransfer object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put("/v1/account/transfer/response", body=kwargs)
        return WalletTransfer.model_validate(self._extract_data(resp))
