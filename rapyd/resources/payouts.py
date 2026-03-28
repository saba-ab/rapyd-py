"""Payouts resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payout import Payout
from rapyd.resources.base import BaseResource


class PayoutsResource(BaseResource):
    """Interact with the Rapyd Payouts API (``/v1/payouts``)."""

    async def create(self, **kwargs: Any) -> Payout:
        """Create a payout.

        Args:
            beneficiary: Beneficiary token or inline object.
            sender: Sender token or inline object.
            payout_amount: Amount to disburse.
            payout_currency: Currency of the payout.
            payout_method_type: Payout method type string.
            ewallet: Source eWallet token.
            sender_currency: Currency of the sender.
            sender_country: Country of the sender.

        Returns:
            Payout object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/payouts", body=kwargs)
        return Payout.model_validate(self._extract_data(resp))

    async def get(self, payout_id: str) -> Payout:
        """Retrieve a payout by ID.

        Args:
            payout_id: The payout token.

        Returns:
            Payout object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/payouts/{payout_id}")
        return Payout.model_validate(self._extract_data(resp))

    async def update(self, payout_id: str, **kwargs: Any) -> Payout:
        """Update a payout.

        Args:
            payout_id: The payout token.
            metadata: Updated metadata.

        Returns:
            Updated Payout object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/payouts/{payout_id}", body=kwargs)
        return Payout.model_validate(self._extract_data(resp))

    async def cancel(self, payout_id: str) -> Payout:
        """Cancel a payout.

        Args:
            payout_id: The payout token.

        Returns:
            Canceled Payout object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/payouts/{payout_id}")
        return Payout.model_validate(self._extract_data(resp))

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Payout]:
        """List payouts with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Payout objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/payouts", params=params)
        data = self._extract_data(resp)
        return [Payout.model_validate(item) for item in (data or [])]

    async def confirm(self, payout_id: str) -> Payout:
        """Confirm a payout (required when confirm_automatically is false).

        Args:
            payout_id: The payout token.

        Returns:
            Confirmed Payout object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post(f"/v1/payouts/confirm/{payout_id}")
        return Payout.model_validate(self._extract_data(resp))

    async def complete(self, payout_id: str, amount: float) -> Payout:
        """Complete a payout in sandbox.

        Args:
            payout_id: The payout token.
            amount: Amount to complete.

        Returns:
            Completed Payout object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post(f"/v1/payouts/complete/{payout_id}/{amount}")
        return Payout.model_validate(self._extract_data(resp))

    async def set_response(self, payout_id: str, **kwargs: Any) -> Payout:
        """Set the beneficiary response for a payout.

        Args:
            payout_id: The payout token.
            status: Response status.

        Returns:
            Updated Payout object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post(f"/v1/payouts/{payout_id}/beneficiary/response", body=kwargs)
        return Payout.model_validate(self._extract_data(resp))
