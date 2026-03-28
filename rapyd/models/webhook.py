"""Pydantic model for Rapyd Webhook Events."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from rapyd.models.base import RapydModel

T = TypeVar("T")


class WebhookEvent(RapydModel, Generic[T]):
    """A single Rapyd webhook event."""

    id: str = ""
    type: str = ""
    data: T | None = None
    trigger_operation_id: str = ""
    status: str = ""
    created_at: int = 0
    # Allow extra fields Rapyd may add
    log: dict[str, Any] | None = None
