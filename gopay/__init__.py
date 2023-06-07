from gopay.api import GoPay
from gopay.payments import Payments
from gopay.models import GopayConfig


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

    gopay = GoPay(config, services or {})
    return Payments(gopay)
