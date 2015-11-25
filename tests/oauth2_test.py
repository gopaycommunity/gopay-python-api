import unittest
from hamcrest import *
from gopay.oauth2 import OAuth2

class OAuth2Test(unittest.TestCase):

    def setUp(self):
        self.browser = GoPaySpy({
            'clientId': 'userId',
            'clientSecret': 'pass',
            'scope': 'irrelevant scope'
        })

    def test_should_call_api_with_basic_authorization(self):
        self.authorize()
        assert_that(self.browser.request, is_((
            'oauth2/token',
            'application/x-www-form-urlencoded',
            'Basic dXNlcklkOnBhc3M=',
            {
                'grant_type': 'client_credentials',
                'scope': 'irrelevant scope'
            }
        )))

    def test_should_return_expired_token_when_api_failed(self):
        self.browser.given_response(False)
        token = self.authorize()
        assert_that(token.token, is_(None))
        assert_that(token.is_expired(), is_(True))

    def test_should_return_extract_token_from_response(self):
        self.browser.given_response(True, {'access_token': 'irrelevant token'})
        token = self.authorize()
        assert_that(token.is_expired(), is_(False))
        assert_that(token.token, is_('irrelevant token'))

    def authorize(self):
        oauth = OAuth2(self.browser)
        return oauth.authorize()


class GoPaySpy:
    def __init__(self, config):
        self.request = []
        self.config = config
        self.response = MockResponse()

    def given_response(self, has_succeed, json = None):
        self.response.result = has_succeed
        self.response.json = json

    def call(self, *args):
        self.request = args
        return self.response

class MockResponse:
    def __init__(self):
        self.result = False
        self.json = None

    def has_succeed(self):
        return self.result
