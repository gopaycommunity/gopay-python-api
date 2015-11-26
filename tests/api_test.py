import unittest
from hamcrest import *
from unittest_data_provider import data_provider
from gopay.api import GoPay,JSON,FORM

class GoPayTest(unittest.TestCase):

    def setUp(self):
        self.browser = BrowserSpy()

    methods = lambda: (
        ({'isProductionMode': True}, 'https://gate.gopay.cz', 'post', {'irrelevant': 'value'}),
        ({'isProductionMode': False}, 'https://gw.sandbox.gopay.com', 'get', None),
    )

    @data_provider(methods)
    def test_should_build_request(self, config, expected_url, expected_method, data):
        self.call(config, 'irrelevant content-type', data)
        assert_that(self.browser.request.url, is_(expected_url + '/api/URL'))
        assert_that(self.browser.request.method, is_(expected_method))
        assert_that(self.browser.request.headers, is_({
            'Accept': 'application/json',
            'Content-Type': 'irrelevant content-type',
            'Authorization': 'irrelevant authorization'
        }))


    types = lambda: (
        (FORM, {'irrelevant': 'value'}),
        (JSON, '{"irrelevant": "value"}'),
    )

    @data_provider(types)
    def  test_should_encode_data(self, content_type, expected_body):
        self.call({'isProductionMode': False}, content_type, {'irrelevant': 'value'})
        assert_that(self.browser.request.body, is_(expected_body))

    def call(self, config, content_type, data):
        gopay = GoPay(config, self.browser)
        gopay.call('URL', content_type, 'irrelevant authorization', data)


class BrowserSpy:
    def __init__(self):
        self.request = None
        self.response = 'irrelevant browser response'

    def browse(self, request):
        self.request = request
        return self.response
