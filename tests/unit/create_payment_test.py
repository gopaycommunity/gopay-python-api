import unittest
import gopay
from tests.unit.utils import Utils


class TestCreatePayment(unittest.TestCase):

    """ TestCreatePayment class
    
    To execute test for certain method properly it is necessary to add prefix 'test' to its name.
    
    """

    def setUp(self):
        self.payments = gopay.payments({
            'goid': Utils.GO_ID,
            'clientId': Utils.CLIENT_ID,
            'clientSecret': Utils.CLIENT_SECRET,
            'isProductionMode': False
        })

    def test_create_payment(self):
        base_payment = Utils.create_base_payment()

        response = self.payments.create_payment(base_payment)

        if "error_code" not in str(response.json):
            print('Payment: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
            print('Payment gwUrl: ' + str(response.json['gw_url']))
        else:
            print('Error: ' + str(response.json))


