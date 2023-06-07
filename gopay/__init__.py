from gopay.api import GoPay
from gopay.payments import Payments
from gopay.models import GopayConfig
from gopay.services import default_logger, DefaultCache


def payments(config: dict, services: dict | None = None) -> Payments:
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

    if services is None:
        services = {"logger": default_logger, "cache": DefaultCache()}

    gopay = GoPay(config, services)
    return Payments(gopay)
