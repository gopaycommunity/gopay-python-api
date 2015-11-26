import unittest
from hamcrest import *
from unittest_data_provider import data_provider
from gopay.api import GoPay,JSON,FORM,add_defaults
from gopay.enums import Language

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
            'Accept-Language': 'en-US',
            'Content-Type': 'irrelevant content-type',
            'Authorization': 'irrelevant authorization'
        }))

    types = lambda: (
        (FORM, {'irrelevant': 'value'}),
        (JSON, '{"irrelevant": "value"}'),
    )

    @data_provider(types)
    def  test_should_encode_data(self, content_type, expected_body):
        self.call({}, content_type)
        assert_that(self.browser.request.body, is_(expected_body))

    languages = lambda: (
        (Language.CZECH, 'cs-CZ'),
        (Language.SLOVAK, 'cs-CZ'),
        (Language.ENGLISH, 'en-US'),
        (Language.GERMAN, 'en-US'),
        (Language.RUSSIAN, 'en-US'),
        ('unknown', 'en-US'),
        ('', 'en-US'),
    )

    @data_provider(languages)
    def  test_should_localize_error_messages(self, lang, expected_lang):
        self.call({'language': lang})
        assert_that(self.browser.request.headers['Accept-Language'], is_(expected_lang))

    def call(self, config, content_type='irrelevant content-type', data={'irrelevant': 'value'}):
        config = add_defaults(config, {
            'isProductionMode': False,
            'language': Language.ENGLISH
        })
        gopay = GoPay(config, self.browser)
        gopay.call('URL', content_type, 'irrelevant authorization', data)


class BrowserSpy:
    def __init__(self):
        self.request = None
        self.response = 'irrelevant browser response'

    def browse(self, request):
        self.request = request
        return self.response
