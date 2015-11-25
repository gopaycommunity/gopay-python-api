import unittest
from hamcrest import *
from unittest_data_provider import data_provider
from gopay.payments import Payments
from gopay.oauth2 import AccessToken

class PaymentsTest(unittest.TestCase):

    def setUp(self):
        self.browser = BrowserSpy()
        self.auth = AuthStub()
        self.payments = Payments(self.browser, self.auth)

    endpoints = lambda: (
        (lambda p: p.create_payment({'payment': ''}), '', 'application/json', {'payment': ''}),
        (lambda p: p.get_status(3), '/3', 'application/x-www-form-urlencoded', None),
        (lambda p: p.refund_payment(3, 100), '/3/refund', 'application/x-www-form-urlencoded', {'amount': 100}),
        (lambda p: p.create_recurrence(3, {'payment': ''}), '/3/create-recurrence', 'application/json', {'payment': ''}),
        (lambda p: p.void_recurrence(3), '/3/void-recurrence', 'application/x-www-form-urlencoded', {}),
        (lambda p: p.capture_authorization(3), '/3/capture', 'application/x-www-form-urlencoded', {}),
        (lambda p: p.void_authorization(3), '/3/void-authorization', 'application/x-www-form-urlencoded', {}),
    )

    @data_provider(endpoints)
    def test_should_build_request(self, call_api, url, type, expected_body):
        self.auth.when_auth_succeed()
        call_api(self.payments)
        assert_that(self.browser.request, is_((
            'payments/payment' + url,
            type,
            'Bearer irrelevant token',
            expected_body
        )))

    def test_should_call_api_when_auth_succeed(self):
        self.auth.when_auth_succeed()
        response = self.payments.create_payment({})
        assert_that(response, is_(self.browser.response))

    def test_should_return_token_response_when_auth_failed(self):
        self.auth.when_auth_failed()
        response = self.payments.create_payment({})
        assert_that(response, is_(self.auth.token.response))


class BrowserSpy:
    def __init__(self):
        self.request = None
        self.response = 'irrelevant browser response'

    def call(self, *args):
        self.request = args
        return self.response


class AuthStub:
    def __init__(self):
        self.token = AccessToken()
        self.token.response = 'irrelevant token response'

    def when_auth_succeed(self):
        self.token.token = 'irrelevant token'

    def when_auth_failed(self):
        self.token.token = None

    def authorize(self):
        return self.token