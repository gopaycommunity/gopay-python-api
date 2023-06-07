from __future__ import annotations
from gopay import enums

from pydantic import BaseModel, Extra


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
