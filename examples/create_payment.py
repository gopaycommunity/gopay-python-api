import gopay
from gopay.enums import BankSwiftCode, Currency, Language, PaymentInstrument, Recurrence

payments = gopay.payments(
    {
        "goid": "my goid",
        "client_id": "my id",
        "client_secret": "my secret",
        "gateway_url": "https://gw.sandbox.gopay.com/",
    }
)

# recurrent payment must have field ''
recurrentPayment = {
    "recurrence": {
        "recurrence_cycle": Recurrence.DAILY,
        "recurrence_period": "7",
        "recurrence_date_to": "2015-12-31",
    }
}

# pre-authorized payment must have field 'preauthorization'
preauthorized_payment = {"preauthorization": True}

response = payments.create_payment(
    {
        "payer": {
            "default_payment_instrument": PaymentInstrument.BANK_ACCOUNT,
            "allowed_payment_instruments": [PaymentInstrument.BANK_ACCOUNT],
            "default_swift": BankSwiftCode.FIO_BANKA,
            "allowed_swifts": [BankSwiftCode.FIO_BANKA, BankSwiftCode.MBANK],
            "contact": {
                "first_name": "Zbynek",
                "last_name": "Zak",
                "email": "zbynek.zak@gopay.cz",
                "phone_number": "+420777456123",
                "city": "C.Budejovice",
                "street": "Plana 67",
                "postal_code": "373 01",
                "country_code": "CZE",
            },
        },
        "amount": 150,
        "currency": Currency.CZECH_CROWNS,
        "order_number": "001",
        "order_description": "pojisteni01",
        "items": [
            {"name": "item01", "amount": 50},
            {"name": "item02", "amount": 100},
        ],
        "additional_params": [{"name": "invoicenumber", "value": "2015001003"}],
        "callback": {
            "return_url": "http://www.your-url.tld/return",
            "notification_url": "http://www.your-url.tld/notify",
        },
        "lang": Language.CZECH,  # if lang is not specified, then default lang is used
    }
)

if response.has_succeed():
    print("hooray, API returned " + str(response))
else:
    print("oops, API returned " + str(response.status_code) + ": " + str(response))
