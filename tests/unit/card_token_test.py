import unittest
import gopay
from tests.unit.utils import Utils
from gopay.enums import PaymentInstrument, Currency, Language


class TestCardToken(unittest.TestCase):

    """ TestCardToken class

    To execute test for certain method properly it is necessary to add prefix 'test' to its name.

    """

    def setUp(self):
        self.payments = gopay.payments({
            'goid': Utils.GO_ID,
            'clientId': Utils.CLIENT_ID,
            'clientSecret': Utils.CLIENT_SECRET,
            'isProductionMode': False
        })

    @staticmethod
    def create_base_card_token_payment():
        base_payment = {
            'payer': {
                'allowed_payment_instruments': [PaymentInstrument.PAYMENT_CARD],
                'default_payment_instrument': PaymentInstrument.PAYMENT_CARD,
                'contact': {
                    'first_name': 'Jarda',
                    'last_name': 'Sokol',
                    'email': 'test-sokol26@test.cz',
                },
                'allowed_card_token': 'VUHweq2TUuQpgU6UaD4c+123xzUwTBXiZK7jHhW7rhSbUb07XcG69Q0cwTxTYvBG3qyym3sJ5zphQS4vL0kEHvvinxXYMqkZtx4rBA9mtZj9JSpy4cIHkXnH3gR+i6CoQ4M+zI2EXGJ+TQ==',
                # 'verify_pin': '',
            },
            'order_number': '6789',
            'amount': '3000',
            'currency': Currency.CZECH_CROWNS,
            'order_description': '6789Description',
            'lang': Language.CZECH,  # if lang is not specified, then default lang is used
            'additional_params': [
                {'name': 'AdditionalKey', 'value': 'AdditionalValue'}
            ],
            'items': [
                {'name': 'Item01', 'amount': '3000', 'count' : '1'},
            ],
            'callback': {
                'return_url': 'https://eshop123.cz/return',
                'notification_url': 'https://eshop123.cz/notify'
            },
        }
        return base_payment

    # All fields on gateway are pre-filled with using card-token.
    def test_payment_with_card_token(self):
        base_payment = self.create_base_card_token_payment()

        response = self.payments.create_payment(base_payment)

        if "error_code" not in str(response.json):
            print('Payment: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
            print('Payment gwUrl: ' + str(response.json['gw_url']))
        else:
            print('Error: ' + str(response.json))

    # After payment completion the used card-token can be found in created payment.
    def test_card_token_payment_status(self):
        payment_id = 3052266451
        response = self.payments.get_status(payment_id)

        if "error_code" not in str(response.json):
            print('Payment: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
            print('Payment gwUrl: ' + str(response.json['gw_url']))
            print('Payment state: ' + str(response.json['state']))
            print('PayerCard - card token: ' + str(response.json['payer']['payment_card']['card_token']))
            print('Payer 3DS Result: ' + str(response.json['payer']['payment_card']['3ds_result']))
        else:
            print('Error: ' + str(response.json))
