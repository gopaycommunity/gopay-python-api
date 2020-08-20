import unittest
import gopay
from utils import Utils


class TestRefund(unittest.TestCase):

    """ TestRefund class
    
    To execute test for certain method properly it is necessary to add prefix 'test' to its name.
    
    """

    def setUp(self):
        self.payments = gopay.payments({
            'goid': Utils.GO_ID,
            'clientId': Utils.CLIENT_ID,
            'clientSecret': Utils.CLIENT_SECRET,
            'isProductionMode': False
        })

    def refund_payment(self):
        payment_id = 3049525986

        response = self.payments.refund_payment(payment_id, 1900)

        if "error_code" not in str(response.json):
            print('Response: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
        else:
            print('Error: ' + str(response.json))
