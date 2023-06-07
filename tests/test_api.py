from gopay.api import GoPay
from gopay.enums import ContentType, Language, TokenScope
from gopay.http import ApiClient, Response


class TestApi:
    def test_gopay(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        gopay = GoPay(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": gateway_url,
                "scope": TokenScope.ALL,
            }
        )

        assert isinstance(gopay, GoPay)
        assert isinstance(gopay.api_client, ApiClient)

    def test_urls(
        self, client_id: str, client_secret: str, goid: str, gateway_url: str
    ):
        with_short_url = GoPay(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": "https://gw.sandbox.gopay.com",
                "scope": TokenScope.ALL,
            }
        )

        assert with_short_url.base_url == gateway_url

        with_short_url_slash = GoPay(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": "https://gw.sandbox.gopay.com/",
                "scope": TokenScope.ALL,
            }
        )

        assert with_short_url_slash.base_url == gateway_url

        with_long_url = GoPay(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": "https://gw.sandbox.gopay.com/api",
                "scope": TokenScope.ALL,
            }
        )

        assert with_long_url.base_url == gateway_url

        with_long_url_slash = GoPay(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": "https://gw.sandbox.gopay.com/api/",
                "scope": TokenScope.ALL,
            }
        )

        assert with_long_url_slash.base_url == gateway_url

    def test_call(
        self,
        client_id: str,
        client_secret: str,
        goid: str,
        gateway_url: str,
        base_payment: dict,
    ):
        base_payment.update({"target": {"type": "ACCOUNT", "goid": goid}})
        gopay = GoPay(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "goid": goid,
                "gateway_url": gateway_url,
                "scope": TokenScope.ALL,
                "language": Language.CZECH,
            }
        )

        response = gopay.call(
            "POST", "/payments/payment", ContentType.JSON, base_payment
        )

        assert isinstance(response, Response)
        assert response.success
