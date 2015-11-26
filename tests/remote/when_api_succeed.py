import unittest
import time
from tests.remote import given_client, should_return
from hamcrest import contains_string, is_
from gopay.enums import Currency


class WhenApiSucceedTest(unittest.TestCase):
    def test_create_payment_and_get_status(self):
        gopay = given_client()

        payment = gopay.create_payment({
            'amount': 1,
            'currency': Currency.CZECH_CROWNS,
            'order_number': 'order-test - ' + time.strftime("%Y-%m-%d %H:%M:%S"),
            'order_description': 'python test',
            'callback': {
                'return_url': 'http://www.your-url.tld/return',
                'notification_url': 'http://www.your-url.tld/notify'
            }
        })
        should_return(payment, 'gw_url', contains_string('.gopay.'))

        id_payment = payment.json['id']
        status = gopay.get_status(id_payment)
        should_return(status, 'state', is_('CREATED'))
