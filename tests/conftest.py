import os

import pytest

import gopay
from gopay.enums import BankSwiftCode, Currency, Language, PaymentInstrument
from gopay.http import Request, Response


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


@pytest.fixture(scope="class")
def payments(
    goid: str, client_id: str, client_secret: str, gateway_url: str
) -> gopay.Payments:
    payments = gopay.payments(
        {
            "goid": goid,
            "client_id": client_id,
            "client_secret": client_secret,
            "gateway_url": gateway_url,
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
        #        PaymentInstrument.TWISTO,
        #        PaymentInstrument.SKIPPAY
            ],
        #    "default_payment_instrument": PaymentInstrument.TWISTO,
            "allowed_swifts": [
                BankSwiftCode.CESKA_SPORITELNA,
                BankSwiftCode.RAIFFEISENBANK,
            ],
        #    "allowed_bnpl_types": ["THIRDS", "LATER"],
        #    "default_bnpl_type": "THIRDS",
            "default_swift": BankSwiftCode.CESKA_SPORITELNA,
            "default_payment_instrument": PaymentInstrument.BANK_ACCOUNT,
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


@pytest.fixture
def mock_request() -> Request:
    request = Request(method="test", path="/test")
    return request


@pytest.fixture
def mock_response() -> Response:
    response = Response(raw_body=b"test", json={}, status_code=0)
    return response
