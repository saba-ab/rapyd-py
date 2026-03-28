"""Plans resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.payment import Plan
from rapyd.resources.base import BaseResource


class PlansResource(BaseResource):
    """Interact with the Rapyd Plans API (``/v1/plans``)."""

    async def create(self, **kwargs: Any) -> Plan:
        """Create a plan.

        Args:
            amount: Plan amount.
            currency: ISO 4217 currency code.
            interval: Billing interval (day, week, month, year).
            product: Product token.

        Returns:
            Plan object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/plans", body=kwargs)
        return Plan.model_validate(self._extract_data(resp))

    async def get(self, plan_id: str) -> Plan:
        """Retrieve a plan by ID.

        Args:
            plan_id: The plan token.

        Returns:
            Plan object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/plans/{plan_id}")
        return Plan.model_validate(self._extract_data(resp))

    async def update(self, plan_id: str, **kwargs: Any) -> Plan:
        """Update a plan.

        Args:
            plan_id: The plan token.
            nickname: Updated nickname.
            metadata: Updated metadata.

        Returns:
            Updated Plan object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put(f"/v1/plans/{plan_id}", body=kwargs)
        return Plan.model_validate(self._extract_data(resp))

    async def delete(self, plan_id: str) -> dict[str, Any]:
        """Delete a plan.

        Args:
            plan_id: The plan token.

        Returns:
            Deletion confirmation dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._delete(f"/v1/plans/{plan_id}")
        return self._extract_data(resp)

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Plan]:
        """List plans with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Plan objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/plans", params=params)
        data = self._extract_data(resp)
        return [Plan.model_validate(item) for item in (data or [])]
