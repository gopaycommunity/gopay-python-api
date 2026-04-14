from datetime import datetime

import pytest
import gopay
from gopay.enums import Language, TokenScope
from gopay.http import AccessToken, Request, Response
from gopay.models import DEFAULT_TIMEOUT
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
                "timeout": 300
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

    def test_default_timeout(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        """When no timeout is specified, the default value from DEFAULT_TIMEOUT is used."""
        payments = gopay.payments(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": gateway_url,
            }
        )
        assert payments.gopay.api_client.timeout == DEFAULT_TIMEOUT

    def test_custom_timeout(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        """Custom timeout specified in config is correctly propagated to ApiClient."""
        custom_timeout = 60
        payments = gopay.payments(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": gateway_url,
                "timeout": custom_timeout,
            }
        )
        assert payments.gopay.api_client.timeout == custom_timeout

    def test_timeout_is_passed_to_full_config(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        """Timeout in full config (with all optional fields) is correctly propagated."""
        payments = gopay.payments(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": gateway_url,
                "scope": TokenScope.ALL,
                "language": Language.CZECH,
                "timeout": 3600,
            }
        )
        assert payments.gopay.api_client.timeout == 3600

    def test_invalid_timeout_zero(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        """Timeout of 0 is rejected by Pydantic validation (must be > 0)."""
        with pytest.raises(Exception):
            gopay.payments(
                {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "goid": goid,
                    "gateway_url": gateway_url,
                    "timeout": 0,
                }
            )

    def test_invalid_timeout_negative(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        """Negative timeout is rejected by Pydantic validation (must be > 0)."""
        with pytest.raises(Exception):
            gopay.payments(
                {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "goid": goid,
                    "gateway_url": gateway_url,
                    "timeout": -10,
                }
            )

