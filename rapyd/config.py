"""Rapyd SDK configuration using pydantic-settings."""

from __future__ import annotations

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class RapydSettings(BaseSettings):
    """Configuration for the Rapyd SDK.

    Values are read from environment variables or a `.env` file.
    All variables are prefixed with ``RAPYD_`` automatically.
    """

    rapyd_access_key: str
    rapyd_secret_key: str
    rapyd_environment: Literal["sandbox", "production"] = "sandbox"
    rapyd_timeout: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def base_url(self) -> str:
        """Return the API base URL for the configured environment."""
        if self.rapyd_environment == "production":
            return "https://api.rapyd.net"
        return "https://sandboxapi.rapyd.net"
