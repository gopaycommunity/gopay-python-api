import unittest
from tests.remote import given_client, should_return_error

class WhenApiFailedTest(unittest.TestCase):

    def test_status_of_non_existent_payment(self):
        gopay = given_client()
        non_existent_id = -10
        status = gopay.get_status(non_existent_id)
        should_return_error(status, 500, {
            'scope': 'G',
            'field': None,
            'error_code': 500,
            'error_name': None,
            'message': None,
            'description': None
        })
