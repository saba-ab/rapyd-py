"""Fraud resource."""

from __future__ import annotations

from typing import Any

from rapyd.resources.base import BaseResource


class FraudResource(BaseResource):
    """Interact with the Rapyd Fraud Protection API (``/v1/fraud/merchant/settings``)."""

    async def get_settings(self) -> dict[str, Any]:
        """Get current fraud protection settings.

        Returns:
            Dict with fraud settings.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get("/v1/fraud/merchant/settings")
        return self._extract_data(resp)

    async def update_settings(self, **kwargs: Any) -> dict[str, Any]:
        """Update fraud protection settings.

        Args:
            Keyword arguments for the settings to update.

        Returns:
            Updated fraud settings dict.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._put("/v1/fraud/merchant/settings", body=kwargs)
        return self._extract_data(resp)
