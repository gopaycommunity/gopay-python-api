import unittest
import gopay
from utils import Utils
from gopay.enums import SupercashSubType


class SupercashMethodsTests(unittest.TestCase):

    """ TestCommonMethods class

    To execute test for certain method properly it is necessary to add prefix 'test' to its name.

    """

    def setUp(self):
        self.payments = gopay.payments({
            'goid': Utils.GO_ID,
            'clientId': Utils.CLIENT_ID,
            'clientSecret': Utils.CLIENT_SECRET,
            'isProductionMode': False
        })

    def test_get_supercash_coupon_batch_status(self):
        batch_id = 961667719

        response = self.payments.get_supercash_coupon_batch_status(batch_id)

        if "error_code" not in str(response.json):
            print('SC batch result: ' + str(response.json))
        else:
            print('Error: ' + str(response.json))

    def test_get_suppercash_coupon_batch(self):
        batch_id = 961667719

        response = self.payments.get_supercash_coupon_batch(batch_id)

        if "error_code" not in str(response.json):
            print('SC batch: ' + str(response.json))
        else:
            print('Error: ' + str(response.json))

    def test_find_supercash_coupons(self):
        payment_session_id = [3050857992, 3050858018]
        #payment_session_id = 3050857992

        response = self.payments.find_supercash_coupons(payment_session_id)

        if "error_code" not in str(response.json):
            print('SC coupons: ' + str(response.json))
        else:
            print('Error: ' + str(response.json))

    def test_get_supercash_coupon(self):
        coupon_id = 100154175

        response = self.payments.get_supercash_coupon(coupon_id)

        if "error_code" not in str(response.json):
            print('SC coupon: ' + str(response.json))
        else:
            print('Error: ' + str(response.json))
