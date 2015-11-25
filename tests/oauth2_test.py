import unittest
from hamcrest import *
from gopay.oauth2 import OAuth2, AccessToken
from gopay.gopay import GoPay

class OAuth2Test(unittest.TestCase):

    def setUp(self):
        self.browser = BrowserSpy()

    def test_should_call_api_and_return_access_token(self):
        token = self.authorize()
        assert_that(token, is_(instance_of(AccessToken)))
        assert_that(self.browser.request.url, is_('https://gw.sandbox.gopay.com/api/oauth2/token'))
        assert_that(self.browser.request.method, is_('post'))
        assert_that(self.browser.request.headers, is_({
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic dXNlcklkOnBhc3M='
        }))
        assert_that(self.browser.request.body, is_({
            'grant_type': 'client_credentials',
            'scope': 'irrelevant scope'
        }))

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
        oauth = OAuth2(
            GoPay(
                {
                    'clientId': 'userId',
                    'clientSecret': 'pass',
                    'scope': 'irrelevant scope'
                },
                self.browser
            )
        )
        return oauth.authorize()


class BrowserSpy:
    def __init__(self):
        self.request = None
        self.response = MockResponse()

    def given_response(self, has_succeed, json = None):
        self.response.result = has_succeed
        self.response.json = json

    def browse(self, request):
        self.request = request
        return self.response

class MockResponse:
    def __init__(self):
        self.result = False
        self.json = None

    def has_succeed(self):
        return self.result
