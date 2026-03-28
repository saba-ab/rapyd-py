"""Rapyd SDK exception hierarchy."""

from __future__ import annotations


class RapydException(Exception):
    """Base exception for all Rapyd SDK errors."""


class RapydApiError(RapydException):
    """Raised when the Rapyd API returns a non-SUCCESS status."""

    def __init__(
        self,
        message: str = "",
        *,
        error_code: str = "",
        status_code: int = 0,
        operation_id: str = "",
        raw: dict | None = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.operation_id = operation_id
        self.raw = raw or {}
        super().__init__(message)

    def __repr__(self) -> str:
        return (
            f"RapydApiError(error_code={self.error_code!r}, status_code={self.status_code}, "
            f"operation_id={self.operation_id!r}, message={self.message!r})"
        )


class RapydAuthError(RapydApiError):
    """Raised on authentication/authorization failures (401/403)."""


class RapydValidationError(RapydException):
    """Raised when request data fails local validation."""

    def __init__(self, message: str = "", *, field: str = "") -> None:
        self.message = message
        self.field = field
        super().__init__(message)


class RapydWebhookError(RapydException):
    """Raised when webhook signature verification fails."""


class RapydTimeoutError(RapydException):
    """Raised when an HTTP request times out."""


class RapydConnectionError(RapydException):
    """Raised when an HTTP connection fails."""
