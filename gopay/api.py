from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from gopay.enums import ContentType, Language
from gopay.http import ApiClient, JSONDict, Request, Response
from gopay.models import DEFAULT_TIMEOUT
from gopay.utils import DEFAULT_USER_AGENT


@dataclass
class GoPay:
    """
    This class saves the basic configuration, sets the base_url and passes requests
    to the API Client
    """

    # Validated configuration as produced by `GopayConfig.model_dump()`
    config: dict[str, Any]
    # Optional services: "logger" (LoggerType) and "cache" (AbstractCache)
    # The declared type applies; Pyright only infers `dict[Unknown, Unknown]` for the
    # bare `dict` factory. Kept as `dict` to leave the runtime default_factory unchanged.
    # (fmt: off keeps the ignore comment on the line Pyright reports.)
    # fmt: off
    services: dict[str, Any] = field(  # pyright: ignore[reportUnknownVariableType]
        default_factory=dict
    )
    # fmt: on
    base_url: str = field(default="", init=False)
    api_client: ApiClient = field(init=False)

    def __post_init__(self) -> None:
        # Make sure URL will be in the form of example.com/api
        gateway_url: str = self.config["gateway_url"]
        urlparts = urlsplit(gateway_url)
        self.base_url = urlunsplit((urlparts.scheme, urlparts.netloc, "/api", "", ""))

        # Prepare
        api_client_config: dict[str, Any] = {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "gateway_url": self.base_url,
            "scope": self.config["scope"],
        }

        # Add optional parameters if found
        api_client_config["timeout"] = self.config.get("timeout", DEFAULT_TIMEOUT)

        if (logger := self.services.get("logger")) is not None:
            api_client_config.update({"logger": logger})

        if (cache := self.services.get("cache")) is not None:
            api_client_config.update({"cache": cache})

        # Create the API client
        self.api_client = ApiClient(**api_client_config)

    def call(
        self,
        method: str,
        path: str,
        content_type: ContentType | None = None,
        body: JSONDict | None = None,
        params: JSONDict | None = None,
    ) -> Response:
        """
        Sets some default headers and passes requests to the API Client
        """
        # Build the request
        request = Request(
            method=method,
            path=path,
            content_type=content_type,
            body=body,
            params=params,
        )

        user_agent = self.config.get("custom_user_agent")
        if user_agent is None:
            user_agent = DEFAULT_USER_AGENT
        else:
            user_agent = self.config["custom_user_agent"]

        # Add some default headers
        request.headers = {
            "Accept": "application/json",
            "User-Agent": user_agent,
            "Accept-Language": "cs-CZ"
            if self.config["language"] in [Language.CZECH, Language.SLOVAK]
            else "en-US",
        }
        if content_type is not None:
            request.headers["Content-Type"] = content_type

        return self.api_client.send_request(request)
