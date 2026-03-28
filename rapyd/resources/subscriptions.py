"""Subscriptions resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payment import Subscription
from rapyd.resources.base import BaseResource


class SubscriptionsResource(BaseResource):
    """Interact with the Rapyd Subscriptions API (``/v1/subscriptions``)."""

    async def create(self, **kwargs: Any) -> Subscription:
        """Create a subscription.

        Args:
            customer: Customer token.
            billing: Billing type ("pay_automatically" or "send_invoice").
            subscription_items: List of plan/quantity dicts.

        Returns:
            Subscription object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/subscriptions", body=kwargs)
        return Subscription.model_validate(self._extract_data(resp))

    async def get(self, sub_id: str) -> Subscription:
        """Retrieve a subscription by ID.

        Args:
            sub_id: The subscription token.

        Returns:
            Subscription object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/subscriptions/{sub_id}")
        return Subscription.model_validate(self._extract_data(resp))

    async def update(self, sub_id: str, **kwargs: Any) -> Subscription:
        """Update a subscription.

        Args:
            sub_id: The subscription token.
            metadata: Updated metadata.
            payment_method: New payment method.

        Returns:
            Updated Subscription object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/subscriptions/{sub_id}", body=kwargs)
        return Subscription.model_validate(self._extract_data(resp))

    async def cancel(self, sub_id: str) -> Subscription:
        """Cancel a subscription.

        Args:
            sub_id: The subscription token.

        Returns:
            Canceled Subscription object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/subscriptions/{sub_id}")
        return Subscription.model_validate(self._extract_data(resp))

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Subscription]:
        """List subscriptions with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Subscription objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/subscriptions", params=params)
        data = self._extract_data(resp)
        return [Subscription.model_validate(item) for item in (data or [])]
