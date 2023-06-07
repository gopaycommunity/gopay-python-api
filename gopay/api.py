from typing import Dict
from dataclasses import dataclass, field
from gopay.http import Request, Response, Browser
from gopay.enums import Language
import json
from urllib.parse import urlsplit, urlunsplit
from gopay import models

JSON = "application/json"
FORM = "application/x-www-form-urlencoded"


@dataclass
class GoPay:
    config: dict
    browser: Browser
    _base_url: str = field(default="", init=False)

    def __post_init__(self):
        urlparts = urlsplit(self.config["gateway_url"])
        self._base_url = urlunsplit((urlparts.scheme, urlparts.netloc, "/api", "", ""))

    def url(self, path: str):
        return self._base_url + path

    def call(
        self, method: str, url: str, content_type: str, authorization: str, data: Dict
    ) -> Response:
        request = Request()
        request.url = self.url(url)

        request.headers = {
            "Accept": "application/json",
            "Accept-Language": "cs-CZ"
            if self.config["language"] in [Language.CZECH, Language.SLOVAK]
            else "en-US",
            "Authorization": authorization,
        }
        if content_type:
            request.headers["Content-Type"] = content_type

        request.method = method
        if data is not None:
            request.body = json.dumps(data) if content_type == JSON else data
        return self.browser.browse(request)


@dataclass
class GopayClient:
    config: models.GopayConfig
    _base_url: str = field(default="", init=False)

    def __post_init__(self):
        urlparts = urlsplit(self.config.gateway_url)
        self._base_url = urlunsplit((urlparts.scheme, urlparts.netloc, "/api", "", ""))


def add_defaults(data: dict, defaults: dict) -> dict:
    full = defaults.copy()
    if data is not None:
        full.update(data)
    return full
