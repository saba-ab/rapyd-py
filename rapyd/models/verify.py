"""Pydantic models for Verify (KYC/KYB) domain."""

from __future__ import annotations

from typing import Any

from rapyd.models.base import RapydObject


class Identity(RapydObject):
    """Rapyd Identity Verification object."""

    country: str = ""
    document_type: str = ""
    reference_id: str = ""
    ewallet: str = ""
    contact: str = ""
    status: str = ""
    result: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    created_at: int = 0
    updated_at: int = 0


class VerificationApplication(RapydObject):
    """Rapyd Verification (hosted IDV) Application object."""

    status: str = ""
    reference_id: str = ""
    country: str = ""
    redirect_url: str = ""
    merchant_details: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    created_at: int = 0
