from dataclasses import dataclass, field
from gopay.http import Request, Response, ApiClient
from gopay.enums import Language, ContentType
from urllib.parse import urlsplit, urlunsplit
from gopay.services import default_logger, DefaultCache


@dataclass
class GoPay:
    config: dict
    services: dict = field(default_factory=dict)
    base_url: str = field(default="", init=False)

    def __post_init__(self):
        urlparts = urlsplit(self.config["gateway_url"])
        self.base_url = urlunsplit((urlparts.scheme, urlparts.netloc, "/api", "", ""))
        self.api_client = ApiClient(
            client_id=self.config["client_id"],
            client_secret=self.config["client_secret"],
            gateway_url=self.base_url,
            scope=self.config["scope"],
            logger=self.services.get("logger") or default_logger,
            cache=self.services.get("cache") or DefaultCache(),
        )

    def call(
        self,
        method: str,
        path: str,
        content_type: ContentType | None = None,
        body: dict | None = None,
    ) -> Response:
        request = Request(
            method=method, path=path, content_type=content_type, body=body
        )

        request.headers = {
            "Accept-Language": "cs-CZ"
            if self.config["language"] in [Language.CZECH, Language.SLOVAK]
            else "en-US"
        }

        return self.api_client.send_request(request)
