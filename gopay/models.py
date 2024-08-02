from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from gopay import enums


class GopayModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")


class GopayConfig(GopayModel):
    goid: int
    client_id: str
    client_secret: str
    gateway_url: str
    scope: enums.TokenScope = enums.TokenScope.ALL
    language: enums.Language = enums.Language.CZECH
