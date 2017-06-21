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

    def test_create_supercash_coupon(self):
        base_coupon = {
            'sub_type' : SupercashSubType.SUB_TYPE_POSTPAID,
            'custom_id' : 'ID-123457',
            'amount' : 100,
            'order_number' : '1',
            'order_description' : 'supercash_coupon_test',
            'buyer_email' : 'zakaznik@example.com',
            'buyer_phone' : '+420777123456',
            'date_valid_to' : '2018-12-31',
            'notification_url' : 'http://www.example-notify.cz/supercash',
        }

        response = self.payments.create_supercash_coupon(base_coupon)

        if "error_code" not in str(response.json):
            print('SC Coupon: ' + str(response.json))
            print('SC coupon id: ' + str(response.json['supercash_coupon_id']))
            print('SC number: ' + str(response.json['supercash_number']))
        else:
            print('Error: ' + str(response.json))

    def _create_supercash_batch(self):
        base_batch = {
            'batch_completed_notification_url' : 'http://www.notify.cz/super',
            'defaults' : {
                'sub_type' : SupercashSubType.SUB_TYPE_POSTPAID,
                'amounts' : [300, 400, 500, 600, 700, 800, 900, 1000],
                'order_description' : 'supercash_coupon_batch_test',
            },
            'coupons' : [
                {
                    'buyer_email' : 'zakaznik1@example.com',
                    'custom_id' : 'ID-123457',
                    'buyer_phone' : '+420777666111',
                    'amounts' : [100],
                },
                {
                    'buyer_email' : 'zakaznik2@example.com',
                    'custom_id' : 'ID-123458',
                    'buyer_phone' : '+420777666222',
                    'amounts' : [200],
                },
                {
                    'buyer_email' : 'zakaznik3@example.com',
                    'custom_id' : 'ID-123459',
                    'buyer_phone' : '+420777666333',
                    'amounts' : [300],
                },
            ],
        }

        response = self.payments.create_supercash_batch(base_batch)

        if "error_code" not in str(response.json):
            print('SC batch id: ' + str(response.json))
        else:
            print('Error: ' + str(response.json))

    def _get_supercash_coupon_batch_status(self):
        batch_id = 961667719

        response = self.payments.get_supercash_coupon_batch_status(batch_id)

        if "error_code" not in str(response.json):
            print('SC batch result: ' + str(response.json))
        else:
            print('Error: ' + str(response.json))

    def _get_suppercash_coupon_batch(self):
        batch_id = 961667719

        response = self.payments.get_supercash_coupon_batch(batch_id)

        if "error_code" not in str(response.json):
            print('SC batch: ' + str(response.json))
        else:
            print('Error: ' + str(response.json))

    def _find_supercash_coupons(self):
        payment_session_id = [3050857992, 3050858018]
        #payment_session_id = 3050857992

        response = self.payments.find_supercash_coupons(payment_session_id)

        if "error_code" not in str(response.json):
            print('SC coupons: ' + str(response.json))
        else:
            print('Error: ' + str(response.json))

    def _get_supercash_coupon(self):
        coupon_id = 100154175

        response = self.payments.get_supercash_coupon(coupon_id)

        if "error_code" not in str(response.json):
            print('SC coupon: ' + str(response.json))
        else:
            print('Error: ' + str(response.json))
