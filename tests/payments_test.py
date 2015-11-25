import unittest
from hamcrest import *
from unittest_data_provider import data_provider
from gopay.payments import Payments

class PaymentsTest(unittest.TestCase):

    def setUp(self):
        self.browser = BrowserSpy()
        self.payments = Payments(self.browser)

    def test_should_call_api_and_return_response(self):
        response = self.payments.create_payment({})
        assert_that(response, is_(self.browser.response))

    endpoints = lambda: (
        (lambda p: p.create_payment({'payment': ''}), 'https://gw.sandbox.gopay.com/api/payments/payment', 'post', is_not),
        (lambda p: p.get_status(3), 'https://gw.sandbox.gopay.com/api/payments/payment/3', 'get', is_),
    )

    @data_provider(endpoints)
    def test_should_build_request(self, call_api, url, method, has_body):
        call_api(self.payments)
        assert_that(self.browser.request.url, is_(url))
        assert_that(self.browser.request.method, is_(method))
        assert_that(self.browser.request.headers, is_not({}))
        assert_that(self.browser.request.body, has_body({}))


class BrowserSpy:
    def __init__(self):
        self.request = None
        self.response = 'irrelevant response'

    def browse(self, request):
        self.request = request
        return self.response
