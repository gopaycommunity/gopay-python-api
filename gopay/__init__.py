from gopay.http import Browser, null_logger
from gopay.api import GoPay, add_defaults
from gopay.oauth2 import OAuth2, InMemoryTokenCache, CachedAuth
from gopay.payments import Payments
from gopay.enums import Language, TokenScope
from gopay.models import GopayConfig


def payments(config: dict, services: dict = None) -> Payments:
    for key in tuple(config.keys()):
        if key == "clientId":
            config["client_id"] = config[key]
            del config[key]
        elif key == "clientSecret":
            config["client_secret"] = config[key]
            del config[key]
        elif key == "gatewayUrl":
            config["gateway_url"] = config[key]
            del config[key]

    config_model = GopayConfig.parse_obj(config)
    config = config_model.dict()

    services = add_defaults(
        services, {"logger": null_logger, "cache": InMemoryTokenCache()}
    )
    browser = Browser(services["logger"], config["timeout"])
    gopay = GoPay(config, browser)
    auth = CachedAuth(OAuth2(gopay), services["cache"])
    return Payments(gopay, auth)
