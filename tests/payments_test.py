import unittest
from hamcrest import *
from unittest_data_provider import data_provider
from gopay.payments import Payments,FORM,JSON
from gopay.oauth2 import AccessToken
from test_doubles import GoPayMock

class PaymentsTest(unittest.TestCase):

    def setUp(self):
        self.browser = GoPayMock({
            'language': 'default',
            'goid': 'id',
        })
        self.auth = AuthStub()
        self.payments = Payments(self.browser, self.auth)

    endpoints = lambda: (
        (lambda p: p.create_payment({'payment': '', 'language': '', 'target': ''}), '', JSON, {'payment': '', 'language': '', 'target': ''}),
        (lambda p: p.create_payment({'payment': ''}), '', JSON, {'payment': '', 'target': {'type': 'ACCOUNT', 'goid': 'id'}, 'language': 'default'}),
        (lambda p: p.get_status(3), '/3', FORM, None),
        (lambda p: p.refund_payment(3, 100), '/3/refund', FORM, {'amount': 100}),
        (lambda p: p.create_recurrence(3, {'payment': ''}), '/3/create-recurrence', JSON, {'payment': ''}),
        (lambda p: p.void_recurrence(3), '/3/void-recurrence', FORM, {}),
        (lambda p: p.capture_authorization(3), '/3/capture', FORM, {}),
        (lambda p: p.void_authorization(3), '/3/void-authorization', FORM, {}),
    )

    @data_provider(endpoints)
    def test_should_build_request(self, call_api, url, type, expected_body):
        self.auth.when_auth_succeed()
        call_api(self.payments)
        self.browser.should_be_called_with(
            'payments/payment' + url,
            type,
            'Bearer irrelevant token',
            expected_body
        )

    def test_should_call_api_when_auth_succeed(self):
        self.auth.when_auth_succeed()
        response = self.payments.create_payment({})
        assert_that(response, is_(self.browser.response))

    def test_should_return_token_response_when_auth_failed(self):
        self.auth.when_auth_failed()
        response = self.payments.create_payment({})
        assert_that(response, is_(self.auth.token.response))

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