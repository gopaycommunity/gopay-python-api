import requests
from dataclasses import dataclass, field
from gopay.enums import TokenScope, ContentType
from deprecated import deprecated
from requests import JSONDecodeError
from datetime import datetime
from gopay.services import AbstractCache, LoggerType, DefaultCache, default_logger


@dataclass
class Request:
    method: str
    path: str
    content_type: ContentType | None = None
    headers: dict[str, str] | None = None
    body: dict | None = None
    basic_auth: bool = False


@dataclass
class Response:
    raw_body: bytes
    json: dict
    status_code: int

    @property
    def success(self) -> bool:
        return self.status_code < 400

    @deprecated
    def has_succeed(self) -> bool:
        return self.status_code < 400

    def __str__(self) -> str:
        try:
            return self.raw_body.decode("utf-8")
        except UnicodeDecodeError:
            return self.raw_body.decode("windows-1250")


@dataclass
class AccessToken:
    token: str
    last_updated: datetime
    scope: TokenScope

    @property
    def is_expired(self):
        if self.last_updated:
            delta = datetime.now() - self.last_updated
            return delta.total_seconds() > 1800
        return True

    def __str__(self) -> str:
        return self.token


@dataclass
class ApiClient:
    """
    Class for handling API request and responses to the GoPay system, authorization
    and headers
    """

    client_id: str
    client_secret: str
    gateway_url: str
    scope: TokenScope
    logger: LoggerType = default_logger
    cache: AbstractCache = field(default_factory=DefaultCache)

    def __post_init__(self):
        _ = self.token

    @property
    def token(self) -> AccessToken | None:
        token = self.cache.get_token(self.client)
        if token is not None and not token.is_expired:
            return token
        else:
            response = self._get_token()
            if response.success:
                token = AccessToken(
                    response.json["access_token"], datetime.now(), self.scope
                )
                self.cache.set_token(self.client, token)
                return token
        return None

    @property
    def client(self) -> str:
        return "-".join((self.client_id, self.gateway_url, self.scope))

    def send_request(self, request: Request) -> Response:
        """
        Send a specified Request to the GoPay REST API and process the response
        """

        # Prepare headers based on content type and authorization
        headers = request.headers or {}
        headers.update({"Accept": "application/json", "User-Agent": "GoPay Python SDK"})
        if request.content_type is not None:
            headers["Content-Type"] = request.content_type

        if not request.basic_auth:
            headers["Authorization"] = f"Bearer {self.token}"

        # Send the request with the specified parameters
        r = requests.request(
            method=request.method,
            url=f"{self.gateway_url}{request.path}",
            headers=headers,
            auth=(self.client_id, self.client_secret) if request.basic_auth else None,
            data=request.body if request.content_type == ContentType.FORM else None,
            json=request.body if request.content_type == ContentType.JSON else None,
        )

        # Build Response instance, try to decode body as JSON
        response = Response(raw_body=r.content, json={}, status_code=r.status_code)
        try:
            response.json = r.json()
        except JSONDecodeError:
            pass

        self.logger(request, response)
        return response

    def _get_token(self) -> Response:
        """
        Method to get the access oauth2 token from GoPay REST API
        """
        # Prepare request
        request = Request(
            method="post",
            path="/oauth2/token",
            content_type=ContentType.FORM,
            body={"grant_type": "client_credentials", "scope": self.scope},
            basic_auth=True,
        )
        # Handle response
        response = self.send_request(request)
        self.logger(request, response)
        return response
