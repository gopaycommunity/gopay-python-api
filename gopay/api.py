from typing import Dict

from gopay.http import Request, Response, Browser
from gopay.enums import Language
import json

JSON = 'application/json'
FORM = 'application/x-www-form-urlencoded'


class GoPay:
    def __init__(self, config: dict, browser: Browser) -> None:
        self.browser = browser
        self.config = config

    def url(self, path: str):
        if "gatewayUrl" in self.config:
            host = self.config["gatewayUrl"]
            if host.endswith("/"):
                host = host[:-1]
            if not host.endswith("/api"):
                host += "/api"
            host += "/"
            return host + path
        host = (
            "https://gate.gopay.cz/api/"
            if self.config["isProductionMode"]
            else "https://gw.sandbox.gopay.com/api/"
        )
        return host + path

    def call(self, url: str, content_type: str, authorization: str, data: Dict) -> Response:
        request = Request()
        request.url = self.url(url)

        request.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'cs-CZ' if self.config['language'] in [Language.CZECH, Language.SLOVAK] else 'en-US',
            'Authorization': authorization
        }
        if content_type:
            request.headers["Content-Type"] = content_type

        if data is None:
            request.method = 'get'
        else:
            request.method = 'post'
            request.body = json.dumps(data) if content_type == JSON else data
        return self.browser.browse(request)


def add_defaults(data: dict, defaults: dict) -> dict:
    full = defaults.copy()
    if data is not None:
        full.update(data)
    return full
