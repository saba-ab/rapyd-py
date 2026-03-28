"""Identities resource."""

from __future__ import annotations

from typing import Any

from rapyd.models.verify import Identity
from rapyd.resources.base import BaseResource


class IdentitiesResource(BaseResource):
    """Interact with the Rapyd Identities API (``/v1/identities``)."""

    async def create(self, **kwargs: Any) -> Identity:
        """Create an identity verification.

        Args:
            country: ISO 3166-1 alpha-2 country code.
            document_type: Document type for verification.
            ewallet: eWallet token.
            contact: Contact token.
            reference_id: Your reference ID.

        Returns:
            Identity object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._post("/v1/identities", body=kwargs)
        return Identity.model_validate(self._extract_data(resp))

    async def get(self, identity_id: str) -> Identity:
        """Retrieve an identity verification by ID.

        Args:
            identity_id: The identity token.

        Returns:
            Identity object.

        Rapyd docs: https://docs.rapyd.net
        """
        resp = await self._get(f"/v1/identities/{identity_id}")
        return Identity.model_validate(self._extract_data(resp))

    async def list(
        self,
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> list[Identity]:
        """List identity verifications with optional pagination.

        Args:
            limit: Max results per page.
            page: Page number.
            starting_after: Cursor.
            ending_before: Cursor.

        Returns:
            List of Identity objects.

        Rapyd docs: https://docs.rapyd.net
        """
        params = self._build_list_params(limit, page, starting_after, ending_before)
        resp = await self._get("/v1/identities", params=params)
        data = self._extract_data(resp)
        return [Identity.model_validate(item) for item in (data or [])]
