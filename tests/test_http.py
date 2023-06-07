from datetime import datetime

from gopay.enums import ContentType, TokenScope
from gopay.http import AccessToken, ApiClient, Request, Response
from gopay.services import DefaultCache


class TestHttp:
    def test_request(self):
        request = Request(
            "POST", "/test", ContentType.JSON, {}, {"value": "test"}, False
        )

        assert isinstance(request, Request)

    def test_response(self):
        response = Response(b'{"value": "test"}', {"value": "test"}, status_code=200)

        assert isinstance(response, Response)
        assert response.success

    def test_access_token(self):
        token = AccessToken("test_token", datetime.now(), TokenScope.ALL)

        assert isinstance(token, AccessToken)
        assert not token.is_expired


class TestApiClient:
    def test_api_client(self, client_id: str, client_secret: str, gateway_url: str):
        api_client = ApiClient(client_id, client_secret, gateway_url, TokenScope.ALL)
        assert isinstance(api_client, ApiClient)
        assert isinstance(api_client.cache, DefaultCache)
        assert api_client.client == f"{client_id}-{gateway_url}-{TokenScope.ALL}"
        assert api_client.token is not None

    def test_send_request(
        self,
        goid: str,
        client_id: str,
        client_secret: str,
        gateway_url: str,
        base_payment: dict,
    ):
        base_payment.update({"target": {"type": "ACCOUNT", "goid": goid}})
        api_client = ApiClient(client_id, client_secret, gateway_url, TokenScope.ALL)
        request = Request(
            "POST",
            "/payments/payment",
            ContentType.JSON,
            {"User-Agent": "PyTest", "Accept": "application/json"},
            base_payment,
            False,
        )
        response = api_client.send_request(request)

        assert isinstance(response, Response)
        assert response.success

    def test_wrong_config(self):
        api_client = ApiClient(
            "wrong_id", "wrong_secret", "https://example.com/wrong", TokenScope.ALL
        )
        assert api_client.token is None
