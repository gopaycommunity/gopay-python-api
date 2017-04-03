import unittest
import gopay
from utils import Utils


class TestPreAuthorization(unittest.TestCase):

    def setUp(self):
        self.payments = gopay.payments({
            'goid': Utils.GO_ID,
            'clientId': Utils.CLIENT_ID,
            'clientSecret': Utils.CLIENT_SECRET,
            'isProductionMode': False
        })

    def _create_preauthorized_payment(self):
        base_payment = Utils.create_base_payment()

        base_payment.update({'preauthorization': True})

        response = self.payments.create_payment(base_payment)

        if "error_code" not in str(response.json):
            print('Payment: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
            print('Payment gwUrl: ' + str(response.json['gw_url']))
            print('Payment instrument: ' + ("NONE" if "'payment_instrument'" not in str(response.json) else str(response.json['payment_instrument'])))
            print('PreAuthorization: ' + ("NONE" if "'preauthorization'" not in str(response.json) else str(response.json['preauthorization'])))
        else:
            print('Error: ' + str(response.json))

    def _void_authorization(self):
        authorized_payment_id = 3049519343

        response = self.payments.void_authorization(authorized_payment_id)

        if "error_code" not in str(response.json):
            print('Response: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
        else:
            print('Error: ' + str(response.json))

    def test_capture_payment(self):
        authorized_payment_id = 3049519447

        response = self.payments.capture_authorization(authorized_payment_id)

        if "error_code" not in str(response.json):
            print('Response: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
        else:
            print('Error: ' + str(response.json))