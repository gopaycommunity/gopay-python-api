import unittest
from unittest_data_provider import data_provider
from tests.remote import given_client, should_return_error

class WhenApiFailedTest(unittest.TestCase):

    languages = lambda: (
        ('CS', 'Chybné přihlašovací údaje. Pokuste se provést přihlášení znovu.'),
        ('EN', 'Wrong credentials. Try sign in again.'),
    )

    @data_provider(languages)
    def  test_should_localize_error_messages(self, lang, expected_error):
        gopay = given_client({
            'language': lang,
            'clientSecret': 'invalid secret'
        })
        status = gopay.get_status('irrelevant id is never used because token is not retrieved')
        should_return_error(status, 500, {
            'scope': 'G',
            'field': None,
            'error_code': 403,
            'error_name': 'AUTH_WRONG_CREDENTIALS',
            'message': expected_error,
            'description': None
        })

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
