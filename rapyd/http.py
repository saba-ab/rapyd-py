"""Internal async HTTP client for the Rapyd API."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx

from rapyd.auth import sign_request
from rapyd.config import RapydSettings
from rapyd.exceptions import (
    RapydApiError,
    RapydAuthError,
    RapydConnectionError,
    RapydTimeoutError,
)


class RapydHttpClient:
    """Low-level async HTTP client that handles signing, envelopes, and errors."""

    def __init__(self, settings: RapydSettings) -> None:
        self._settings = settings
        self._client = httpx.AsyncClient(
            base_url=settings.base_url,
            timeout=httpx.Timeout(settings.rapyd_timeout),
            headers={"Content-Type": "application/json"},
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Execute a signed request against the Rapyd API."""
        # Build query string and append to path for signing
        sign_path = path
        if params:
            cleaned = {k: v for k, v in params.items() if v is not None}
            if cleaned:
                sign_path = f"{path}?{urlencode(cleaned)}"

        auth = sign_request(
            http_method=method,
            url_path=sign_path,
            access_key=self._settings.rapyd_access_key,
            secret_key=self._settings.rapyd_secret_key,
            body=body,
        )

        headers: dict[str, str] = {
            "access_key": auth["access_key"],
            "salt": auth["salt"],
            "timestamp": auth["timestamp"],
            "signature": auth["signature"],
        }

        # Auto-generate idempotency key for POST if not provided
        if method.lower() == "post":
            idem = idempotency_key or f"{auth['timestamp']}-{auth['salt']}"
            headers["idempotency"] = idem

        try:
            response = await self._client.request(
                method.upper(),
                sign_path,
                json=body,
                headers=headers,
            )
        except httpx.TimeoutException as exc:
            raise RapydTimeoutError(str(exc)) from exc
        except httpx.ConnectError as exc:
            raise RapydConnectionError(str(exc)) from exc

        data: dict[str, Any] = response.json()
        return self._handle_response(data, response.status_code)

    def _handle_response(self, data: dict[str, Any], status_code: int) -> dict[str, Any]:
        """Check the Rapyd response envelope and raise on errors."""
        status = data.get("status", {})
        if status.get("status") != "SUCCESS":
            error_code = status.get("error_code", "")
            message = status.get("message", "")
            operation_id = status.get("operation_id", "")

            exc_cls = RapydApiError
            if status_code in (401, 403) or error_code in (
                "UNAUTHORIZED_API_CALL",
                "UNAUTHENTICATED",
            ):
                exc_cls = RapydAuthError

            raise exc_cls(
                message,
                error_code=error_code,
                status_code=status_code,
                operation_id=operation_id,
                raw=data,
            )
        return data

    async def get(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a signed GET request."""
        return await self.request("get", path, params=params)

    async def post(
        self,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Execute a signed POST request."""
        return await self.request("post", path, body=body, idempotency_key=idempotency_key)

    async def put(self, path: str, *, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a signed PUT request."""
        return await self.request("put", path, body=body)

    async def delete(self, path: str) -> dict[str, Any]:
        """Execute a signed DELETE request."""
        return await self.request("delete", path)

    async def aclose(self) -> None:
        """Close the underlying httpx client."""
        await self._client.aclose()

    async def __aenter__(self) -> RapydHttpClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()
