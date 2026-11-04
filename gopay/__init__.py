from __future__ import annotations

from typing import Any

# Redundant aliases mark these names as explicit re-exports for type checkers
from gopay.api import GoPay as GoPay
from gopay.models import GopayConfig as GopayConfig
from gopay.payments import Payments as Payments


def payments(
    config: dict[str, Any], services: dict[str, Any] | None = None
) -> Payments:
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
        elif key == "customUserAgent":
            config["custom_user_agent"] = config[key]
            del config[key]

    # Use Pydantic to validate the config object
    config_model = GopayConfig.model_validate(config)
    config = config_model.model_dump()

    # Create and return the Payments and GoPay objects
    gopay = GoPay(config, services or {})
    return Payments(gopay)
