"""Base resource class for all Rapyd API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from rapyd.http import RapydHttpClient


class BaseResource:
    """Base class that all resource classes inherit from."""

    def __init__(self, client: RapydHttpClient) -> None:
        self._client = client

    async def _get(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self._client.get(path, params=params)

    async def _post(
        self,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        return await self._client.post(path, body=body, idempotency_key=idempotency_key)

    async def _put(self, path: str, *, body: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self._client.put(path, body=body)

    async def _delete(self, path: str) -> dict[str, Any]:
        return await self._client.delete(path)

    @staticmethod
    def _build_list_params(
        limit: int | None = None,
        page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> dict[str, Any]:
        """Build pagination query params, only including non-None values."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if page is not None:
            params["page"] = page
        if starting_after is not None:
            params["starting_after"] = starting_after
        if ending_before is not None:
            params["ending_before"] = ending_before
        return params

    @staticmethod
    def _extract_data(response: dict[str, Any]) -> Any:
        """Return the ``data`` field from a Rapyd response envelope."""
        return response.get("data")
