from __future__ import annotations

from pydantic import BaseModel, Extra

from gopay import enums


class GopayModel(BaseModel):
    class Config:
        use_enum_values = True
        extra = Extra.forbid


class GopayConfig(GopayModel):
    goid: int
    client_id: str
    client_secret: str
    gateway_url: str
    scope: enums.TokenScope = enums.TokenScope.ALL
    language: enums.Language = enums.Language.CZECH
