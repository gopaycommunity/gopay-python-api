import unittest
from hamcrest import *
from gopay.oauth2 import OAuth2,FORM
from test_doubles import GoPayMock

class OAuth2Test(unittest.TestCase):

    def setUp(self):
        self.browser = GoPayMock({
            'clientId': 'userId',
            'clientSecret': 'pass',
            'scope': 'irrelevant scope'
        })

    def test_should_call_api_with_basic_authorization(self):
        self.browser.given_response()
        self.authorize()
        self.browser.should_be_called_with(
            'oauth2/token',
            FORM,
            'Basic dXNlcklkOnBhc3M=',
            {
                'grant_type': 'client_credentials',
                'scope': 'irrelevant scope'
            }
        )

    def test_should_return_expired_token_when_api_failed(self):
        self.browser.given_response(False)
        token = self.authorize()
        assert_that(token.token, is_(None))
        assert_that(token.is_expired(), is_(True))

    def test_should_return_extract_token_from_response(self):
        self.browser.given_response(True, {'access_token': 'irrelevant token', 'expires_in': 1800})
        token = self.authorize()
        assert_that(token.is_expired(), is_(False))
        assert_that(token.token, is_('irrelevant token'))
        assert_that(token.expiration_date, is_not(None))

    def authorize(self):
        oauth = OAuth2(self.browser)
        return oauth.authorize()



