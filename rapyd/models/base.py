"""Base Pydantic models for the Rapyd SDK."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class RapydModel(BaseModel):
    """Base model for all Rapyd data objects."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class RapydStatus(RapydModel):
    """Rapyd API response status envelope."""

    error_code: str = ""
    status: str = ""
    message: str = ""
    response_code: str = ""
    operation_id: str = ""

    @property
    def is_success(self) -> bool:
        return self.status == "SUCCESS"

    @property
    def is_error(self) -> bool:
        return self.status == "ERROR"


class RapydResponse(RapydModel, Generic[T]):
    """Generic wrapper for Rapyd API responses."""

    status: RapydStatus = RapydStatus()
    data: T | None = None
    has_more: bool = False
    total_count: int | None = None


class RapydObject(RapydModel):
    """Base model for Rapyd objects that have an ``id`` field."""

    id: str = ""


class RapydAddress(RapydModel):
    """Reusable address model."""

    name: str = ""
    line_1: str = ""
    line_2: str = ""
    city: str = ""
    state: str = ""
    country: str = ""
    zip: str = ""
    phone_number: str = ""
