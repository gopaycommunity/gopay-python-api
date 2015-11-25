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
        call_api(self.payments)
        assert_that(self.browser.request.url, is_('https://gw.sandbox.gopay.com/api/payments/payment' + url))
        assert_that(self.browser.request.method, is_(method))
        assert_that(self.browser.request.headers, is_not({}))
        assert_that(self.browser.request.body, has_empty_body({}))


class BrowserSpy:
    def __init__(self):
        self.request = None
        self.response = 'irrelevant response'

    def browse(self, request):
        self.request = request
        return self.response
