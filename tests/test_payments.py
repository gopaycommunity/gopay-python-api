from datetime import datetime

import gopay
from gopay.enums import Language, TokenScope
from gopay.http import AccessToken, Request, Response, TokenScope
from gopay.payments import Payments
from gopay.services import AbstractCache


def mock_logger(request: Request, response: Response) -> None:
    pass


class MockCache(AbstractCache):
    def get_token(self, key: str) -> AccessToken:
        return AccessToken("test", datetime.now(), TokenScope.ALL)

    def set_token(self, key: str, token: AccessToken) -> None:
        pass


class TestPayments:
    def test_base_config(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        payments = gopay.payments(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": gateway_url,
            }
        )
        assert isinstance(payments, Payments)
        assert payments.gopay.api_client.token is not None

    def test_full_config(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        payments = gopay.payments(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": gateway_url,
                "scope": TokenScope.ALL,
                "language": Language.CZECH,
            }
        )
        assert isinstance(payments, Payments)
        assert payments.gopay.api_client.token is not None

    def test_camelcase_config(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        payments = gopay.payments(
            {
                "clientId": client_id,
                "clientSecret": client_secret,
                "goid": goid,
                "gatewayUrl": gateway_url,
            }
        )
        assert isinstance(payments, Payments)
        assert payments.gopay.api_client.token is not None

    def test_with_services(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        payments = gopay.payments(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": gateway_url,
            },
            {"logger": mock_logger, "cache": MockCache()},
        )

        assert isinstance(payments, Payments)
        assert payments.gopay.api_client.token is not None
        assert isinstance(payments.gopay.api_client.cache, MockCache)
        assert payments.gopay.api_client.logger == mock_logger

    def test_embed_url(self, payments: Payments, gateway_url: str):
        assert payments.get_embedjs_url == gateway_url[:-4] + "/gp-gw/js/embed.js"
