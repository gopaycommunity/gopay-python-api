from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

from gopay import enums

DEFAULT_TIMEOUT = 3600


class GopayModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")


class GopayConfig(GopayModel):
    goid: int
    client_id: str
    client_secret: str
    gateway_url: str
    timeout: int = Field(
        default=DEFAULT_TIMEOUT,
        gt=0,
        description="Request timeout in seconds. Must be a positive integer. Defaults to 30 seconds.",
    )
    scope: enums.TokenScope = enums.TokenScope.ALL
    language: enums.Language = enums.Language.CZECH
    custom_user_agent: Optional[str] = None
