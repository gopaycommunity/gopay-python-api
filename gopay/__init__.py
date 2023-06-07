from __future__ import annotations

from gopay.api import GoPay
from gopay.models import GopayConfig
from gopay.payments import Payments


def payments(config: dict, services: dict | None = None) -> Payments:
    """
    Recommended way of initating the GoPay SDK. This methods handles configuration
    validation and if needed, conversion from camelCase to snake_case
    """
    # If any of the config keys are camelCase, convert them to snake_case
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

    # Use Pydantic to validate the config object
    config_model = GopayConfig.parse_obj(config)
    config = config_model.dict()

    # Create and return the Payments and GoPay objects
    gopay = GoPay(config, services or {})
    return Payments(gopay)
