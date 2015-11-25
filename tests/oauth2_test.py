import unittest
from hamcrest import *
from gopay.oauth2 import OAuth2, AccessToken

class OAuth2Test(unittest.TestCase):

    def test_should_call_api_and_return_access_token(self):
        browser = BrowserSpy()
        oauth = OAuth2(
            {
                'clientId': 'userId',
                'clientSecret': 'pass',
                'scope': 'irrelevant scope'
            },
            browser
        )
        token = oauth.authorize()
        assert_that(token, is_(instance_of(AccessToken)))
        assert_that(browser.request.url, is_('https://gw.sandbox.gopay.com/api/oauth2/token'))
        assert_that(browser.request.method, is_('post'))
        assert_that(browser.request.headers, is_({
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'userId:pass'
        }))
        assert_that(browser.request.body, is_({
            'grant_type': 'client_credentials',
            'scope': 'irrelevant scope'
        }))


class BrowserSpy:
    def __init__(self):
        self.request = None

    def browse(self, request):
        self.request = request
        return MockResponse()

class MockResponse:
    pass