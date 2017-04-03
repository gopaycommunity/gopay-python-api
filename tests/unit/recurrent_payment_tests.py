import unittest
import gopay
from utils import Utils
from gopay.enums import Recurrence


class TestRecurrentPayment(unittest.TestCase):

    def setUp(self):
        self.payments = gopay.payments({
            'goid': Utils.GO_ID,
            'clientId': Utils.CLIENT_ID,
            'clientSecret': Utils.CLIENT_SECRET,
            'isProductionMode': False
        })

    def _create_recurrent_payment(self):
        base_payment = Utils.create_base_payment()

        base_payment.update({'recurrence': {
            'recurrence_cycle': Recurrence.WEEKLY,
            'recurrence_period': "1",
            'recurrence_date_to': '2018-04-01'
        }})

        response = self.payments.create_payment(base_payment)

        if "error_code" not in str(response.json):
            print('Payment: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
            print('Payment gwUrl: ' + str(response.json['gw_url']))
            print('Payment instrument: ' + ("NONE" if "'payment_instrument'" not in str(response.json) else str(response.json['payment_instrument'])))
            print('Recurrence: ' + ("NONE" if "'recurrence'" not in str(response.json) else str(response.json['recurrence'])))
        else:
            print('Error: ' + str(response.json))

    def test_void_recurrence(self):
        recurrent_payment_id = 3049520773

        response = self.payments.void_recurrence(recurrent_payment_id)

        if "error_code" not in str(response.json):
            print('Response: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
        else:
            print('Error: ' + str(response.json))