import unittest
import gopay
from utils import Utils


class TestRefund(unittest.TestCase):

    def setUp(self):
        self.payments = gopay.payments({
            'goid': Utils.GO_ID,
            'clientId': Utils.CLIENT_ID,
            'clientSecret': Utils.CLIENT_SECRET,
            'isProductionMode': False
        })

    def test_refund_payment(self):
        payment_id = 3049525986

        response = self.payments.refund_payment(payment_id, 1900)

        if "error_code" not in str(response.json):
            print('Response: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
        else:
            print('Error: ' + str(response.json))