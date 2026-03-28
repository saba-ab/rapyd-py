"""Verification resource."""

from __future__ import annotations

from typing import Any

from rapyd.resources.base import BaseResource


class VerificationResource(BaseResource):
    """Interact with the Rapyd Verification API (hosted IDV)."""

    async def create_hosted_page(self, **kwargs: Any) -> dict[str, Any]:
        """Create a hosted identity verification page.

        Args:
            country: ISO 3166-1 alpha-2 country code.
            reference_id: Your reference ID.
            ewallet: eWallet token.
            contact: Contact token.

        Returns:
            Dict with redirect_url for the hosted page.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/hosted/idv", body=kwargs)
        return self._extract_data(resp)

    async def get_application_status(self, application_id: str) -> dict[str, Any]:
        """Get the status of a verification application.

        Args:
            application_id: The application token.

        Returns:
            Dict with application status details.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/verify/applications/status/{application_id}")
        return self._extract_data(resp)
