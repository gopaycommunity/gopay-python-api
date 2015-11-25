import unittest
from hamcrest import *
from unittest_data_provider import data_provider
from gopay.payments import Payments
from gopay.oauth2 import AccessToken
from gopay.gopay import GoPay

class PaymentsTest(unittest.TestCase):

    def setUp(self):
        self.browser = BrowserSpy()
        self.auth = AuthStub()
        self.payments = Payments(GoPay({}, self.browser), self.auth)

    endpoints = lambda: (
        (lambda p: p.create_payment({'payment': ''}), '', 'post', is_not),
        (lambda p: p.get_status(3), '/3', 'get', is_),
        (lambda p: p.refund_payment(3, 100), '/3/refund', 'post', is_not),
        (lambda p: p.create_recurrence(3, {'payment': ''}), '/3/create-recurrence', 'post', is_not),
        (lambda p: p.void_recurrence(3), '/3/void-recurrence', 'post', is_),
        (lambda p: p.capture_authorization(3), '/3/capture', 'post', is_),
        (lambda p: p.void_authorization(3), '/3/void-authorization', 'post', is_),
    )

    @data_provider(endpoints)
    def test_should_build_request(self, call_api, url, method, has_empty_body):
        self.auth.when_auth_succeed()
        call_api(self.payments)
        assert_that(self.browser.request.url, is_('https://gw.sandbox.gopay.com/api/payments/payment' + url))
        assert_that(self.browser.request.method, is_(method))
        assert_that(self.browser.request.headers, is_not({}))
        assert_that(self.browser.request.body, has_empty_body({}))

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

    def browse(self, request):
        self.request = request
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