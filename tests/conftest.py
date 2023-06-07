from gopay.enums import PaymentInstrument, BankSwiftCode, Currency, Language
import gopay

import os

import pytest


@pytest.fixture(scope="session")
def goid() -> str:
    goid = os.getenv("GOID")
    if goid is not None:
        return goid
    raise TypeError("Could not find GOID env variable")


@pytest.fixture(scope="session")
def client_id() -> str:
    client_id = os.getenv("CLIENT_ID")
    if client_id is not None:
        return client_id
    raise TypeError("Could not find CLIENT_ID env variable")


@pytest.fixture(scope="session")
def client_secret() -> str:
    client_secret = os.getenv("CLIENT_SECRET")
    if client_secret is not None:
        return client_secret
    raise TypeError("Could not find CLIENT_SECRET env variable")


@pytest.fixture(scope="session")
def gateway_url() -> str:
    gateway_url = os.getenv("GATEWAY_URL")
    if gateway_url is not None:
        return gateway_url
    raise TypeError("Could not find API_URL env variable")


@pytest.fixture(scope="session")
def goid_eet() -> str:
    goid_eet = os.getenv("GOID_EET")
    if goid_eet is not None:
        return goid_eet
    raise TypeError("Could not find GOID_EET env variable")


@pytest.fixture(scope="session")
def client_id_eet() -> str:
    client_id_eet = os.getenv("CLIENT_ID_EET")
    if client_id_eet is not None:
        return client_id_eet
    raise TypeError("Could not find CLIENT_ID_EET env variable")


@pytest.fixture(scope="session")
def client_secret_eet() -> str:
    client_secret_eet = os.getenv("CLIENT_SECRET_EET")
    if client_secret_eet is not None:
        return client_secret_eet
    raise TypeError("Could not find CLIENT_SECRET_EET env variable")


@pytest.fixture(scope="class")
def payments(
    goid: str, client_id: str, client_secret: str, gateway_url: str
) -> gopay.Payments:
    payments = gopay.payments(
        {
            "goid": goid,
            "clientId": client_id,
            "clientSecret": client_secret,
            "gatewayUrl": gateway_url,
        }
    )
    return payments


@pytest.fixture
def base_payment() -> dict:
    base_payment = {
        "payer": {
            "allowed_payment_instruments": [
                PaymentInstrument.BANK_ACCOUNT,
                PaymentInstrument.PAYMENT_CARD,
            ],
            "allowed_swifts": [
                BankSwiftCode.CESKA_SPORITELNA,
                BankSwiftCode.RAIFFEISENBANK,
            ],
            #'default_swift': BankSwiftCode.CESKA_SPORITELNA,
            #'default_payment_instrument': PaymentInstrument.BANK_ACCOUNT,
            "contact": {
                "email": "test.test@gopay.cz",
            },
        },
        "order_number": "6789",
        "amount": "1900",
        "currency": Currency.CZECH_CROWNS,
        "order_description": "6789Description",
        "lang": Language.CZECH,  # if lang is not specified, then default lang is used
        "additional_params": [{"name": "AdditionalKey", "value": "AdditionalValue"}],
        "items": [
            {"name": "Item01", "amount": "1900", "count": "1"},
        ],
        "callback": {
            "return_url": "https://eshop123.cz/return",
            "notification_url": "https://eshop123.cz/notify",
        },
    }
    return base_payment
