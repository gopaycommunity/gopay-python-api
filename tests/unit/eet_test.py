import unittest
import gopay
from tests.unit.utils import Utils
from gopay.enums import (
    PaymentInstrument,
    BankSwiftCode,
    Currency,
    Language,
    VatRate,
    ItemType,
    Recurrence,
)


class TestEET(unittest.TestCase):

    """TestEET class

    To execute test for certain method properly it is necessary to add prefix 'test' to its name.

    """

    def setUp(self):
        self.payments = gopay.payments(
            {
                "goid": Utils.GO_ID_EET,
                "clientId": Utils.CLIENT_ID_EET,
                "clientSecret": Utils.CLIENT_SECRET_EET,
                "gatewayUrl": Utils.GATEWAY_URL,
            }
        )

    def create_base_eet_payment(self):
        base_eet_payment = {
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
            "order_number": "EET6789",
            "amount": "139950",
            "currency": Currency.CZECH_CROWNS,
            "order_description": "EET6789Description",
            "lang": Language.CZECH,  # if lang is not specified, then default lang is used
            "additional_params": [
                {"name": "AdditionalKey", "value": "AdditionalValue"}
            ],
            "items": [
                {
                    "name": "Pocitac Item1",
                    "amount": "119990",
                    "count": "1",
                    "vat_rate": VatRate.RATE_4,
                    "type": ItemType.ITEM,
                    "ean": "1234567890123",
                    "product_url": "https://www.eshop123.cz/pocitac",
                },
                {
                    "name": "Oprava Item2",
                    "amount": "19960",
                    "count": "1",
                    "vat_rate": VatRate.RATE_3,
                    "type": ItemType.ITEM,
                    "ean": "1234567890189",
                    "product_url": "https://www.eshop123.cz/pocitac/oprava",
                },
            ],
            "callback": {
                "return_url": "https://eshop123.cz/return",
                "notification_url": "https://eshop123.cz/notify",
            },
        }
        return base_eet_payment

    def create_eet_payment_object(self, base_eet_payment):
        eet_payment = self.payments.create_payment(base_eet_payment)

        if "error_code" not in str(eet_payment.json):
            print("EET Payment: " + str(eet_payment.json))
            print("EET Payment id: " + str(eet_payment.json["id"]))
            print("EET Payment gwUrl: " + str(eet_payment.json["gw_url"]))
            print("EET: " + str(base_eet_payment["eet"]))
        else:
            print("Error: " + str(eet_payment.json))

        return eet_payment

    def _create_eet_payment(self):
        base_eet_payment = self.create_base_eet_payment()

        base_eet_payment.update(
            {
                "eet": {
                    "celk_trzba": "139950",
                    "zakl_dan1": "99165",
                    "dan1": "20825",
                    "zakl_dan2": "17357",
                    "dan2": "2603",
                    "mena": Currency.CZECH_CROWNS,
                }
            }
        )

        result = self.create_eet_payment_object(base_eet_payment)

    def _create_recurrent_eet_payment(self):
        base_eet_payment = self.create_base_eet_payment()

        # base_eet_payment.update({'recurrence': {
        #     'recurrence_cycle': Recurrence.WEEKLY,
        #     'recurrence_period': "1",
        #     'recurrence_date_to': '2018-04-01'
        # }})

        base_eet_payment.update(
            {
                "recurrence": {
                    "recurrence_cycle": Recurrence.ON_DEMAND,
                    "recurrence_date_to": "2018-04-01",
                }
            }
        )

        base_eet_payment.update(
            {
                "eet": {
                    "celk_trzba": "139950",
                    "zakl_dan1": "99165",
                    "dan1": "20825",
                    "zakl_dan2": "17357",
                    "dan2": "2603",
                    "mena": Currency.CZECH_CROWNS,
                }
            }
        )

        result = self.create_eet_payment_object(base_eet_payment)

        if "error_code" not in str(result.json):
            print(
                "EET Recurrence: "
                + (
                    "NONE"
                    if "'recurrence'" not in str(result.json)
                    else str(result.json["recurrence"])
                )
            )
        else:
            print("Error: " + str(result.json))

    def _next_on_demand_eet(self):
        eet_next_payment = {
            "amount": "2000",
            "currency": "CZK",
            "order_number": "EETOnDemand6789",
            "order_description": "EETOnDemand6789Description",
            "items": [
                {
                    "name": "OnDemand Prodlouzena zaruka",
                    "amount": "2000",
                    "count": "1",
                    "vat_rate": VatRate.RATE_4,
                    "type": ItemType.ITEM,
                    "ean": "1234567890123",
                    "product_url": "https://www.eshop123.cz/pocitac/prodlouzena_zaruka",
                },
            ],
            "eet": {
                "celk_trzba": "2000",
                "zakl_dan1": "1580",
                "dan1": "420",
                "mena": Currency.CZECH_CROWNS,
            },
        }

        eet_on_demand_payment = self.payments.create_recurrence(
            3049524166, eet_next_payment
        )

        if "error_code" not in str(eet_on_demand_payment.json):
            print("EET Payment: " + str(eet_on_demand_payment.json))
            print("EET Payment id: " + str(eet_on_demand_payment.json["id"]))
            print("EET Payment gwUrl: " + str(eet_on_demand_payment.json["gw_url"]))
            print(
                "EET Payment instrument: "
                + (
                    "NONE"
                    if "'payment_instrument'" not in str(eet_on_demand_payment.json)
                    else str(eet_on_demand_payment.json["payment_instrument"])
                )
            )
            print(
                "EET Recurrence: "
                + (
                    "NONE"
                    if "'recurrence'" not in str(eet_on_demand_payment.json)
                    else str(eet_on_demand_payment.json["recurrence"])
                )
            )
        else:
            print("Error: " + str(eet_on_demand_payment.json))

    def test_eet_payment_status(self):
        payment_id = 3049525349
        response = self.payments.get_status(payment_id)

        if "error_code" not in str(response.json):
            print("EET Payment: " + str(response.json))
            print("EET Payment id: " + str(response.json["id"]))
            print("EET Payment gwUrl: " + str(response.json["gw_url"]))
            print("EET Payment state: " + str(response.json["state"]))
            print(
                "EET Payment instrument: "
                + (
                    "NONE"
                    if "'payment_instrument'" not in str(response.json)
                    else str(response.json["payment_instrument"])
                )
            )
            print(
                "EET PreAuthorization: "
                + (
                    "NONE"
                    if "'preauthorization'" not in str(response.json)
                    else str(response.json["preauthorization"])
                )
            )
            print(
                "EET Recurrence: "
                + (
                    "NONE"
                    if "'recurrence'" not in str(response.json)
                    else str(response.json["recurrence"])
                )
            )
            print(
                "EET code: "
                + (
                    "NONE"
                    if "'eet_code'" not in str(response.json)
                    else str(response.json["eet_code"])
                )
            )
        else:
            print("Error: " + str(response.json))

    def _eet_payment_refund(self):
        refund_object = {
            "amount": "139950",
            "items": [
                {
                    "name": "Pocitac Item1",
                    "amount": "119990",
                    "count": "1",
                    "vat_rate": VatRate.RATE_4,
                    "type": ItemType.ITEM,
                    "ean": "1234567890123",
                    "product_url": "https://www.eshop123.cz/pocitac",
                },
                {
                    "name": "Oprava Item2",
                    "amount": "19960",
                    "count": "1",
                    "vat_rate": VatRate.RATE_3,
                    "type": ItemType.ITEM,
                    "ean": "1234567890189",
                    "product_url": "https://www.eshop123.cz/pocitac/oprava",
                },
            ],
            "eet": {
                "celk_trzba": "139950",
                "zakl_dan1": "99165",
                "dan1": "20825",
                "zakl_dan2": "17357",
                "dan2": "2603",
                "mena": Currency.CZECH_CROWNS,
            },
        }

        result = self.payments.refund_payment_eet(3049525349, refund_object)

        if "error_code" not in str(result.json):
            print("Response: " + str(result.json))
            print("EET Payment id: " + str(result.json["id"]))
        else:
            print("Error: " + str(result.json))

    def _eet_receipt_find_by_filter(self):
        receipt_filter = {
            "date_from": "2017-03-02",
            "date_to": "2017-04-02",
            "id_provozovny": "11",
        }

        receipts = self.payments.find_eet_receipts_by_filter(receipt_filter)

        if "error_code" not in str(receipts.json):
            print("Response: " + str(receipts.json))
        else:
            print("Error: " + str(receipts.json))

    def _eet_receipt_find_by_payment_id(self):
        receipt = self.payments.get_eet_receipt_by_payment_id(3048429735)

        if "error_code" not in str(receipt.json):
            print("Response: " + str(receipt.json))
        else:
            print("Error: " + str(receipt.json))
