import unittest
from hamcrest import *
from gopay.oauth2 import *
from test_doubles import GoPayMock
from datetime import datetime, timedelta


class OAuth2Test(unittest.TestCase):
    def setUp(self):
        self.browser = GoPayMock({
            'clientId': 'userId',
            'clientSecret': 'pass',
            'scope': 'irrelevant scope',
            'isProductionMode': False
        })
        self.oauth = OAuth2(self.browser)

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

    def test_should_uniquely_identify_current_client(self):
        assert_that(self.oauth.get_client(), is_('userId-0-irrelevant scope'))

    def authorize(self):
        return self.oauth.authorize()


class CachedOAuthTest(unittest.TestCase):
    def setUp(self):
        self.token = AccessToken()
        self.is_token_in_cache = True
        self.reauthorized_token = 'irrelevant access token'
        self.cache = InMemoryTokenCache()

    def test_should_use_unexpired_token(self):
        self.token.token = 'irrelevant token'
        self.token.expiration_date = datetime.now() + timedelta(days=1)
        self.token_should_be(self.token)

    def test_should_reauthorize_when_token_is_empty(self):
        self.token.token = None
        self.token_should_be(self.reauthorized_token)

    def test_should_reauthorize_when_expiration_is_empty(self):
        self.token.token = 'irrelevant token'
        self.token.expiration_date = None
        self.token_should_be(self.reauthorized_token)

    def test_should_reauthorize_when_token_is_expired(self):
        self.token.token = 'irrelevant token'
        self.token.expiration_date = datetime.now() - timedelta(minutes=1)
        self.token_should_be(self.reauthorized_token)

    def test_should_reauthorize_when_no_token_exists(self):
        self.token = None
        self.token_should_be(self.reauthorized_token)

    def test_should_reauthorize_when_cache_is_empty(self):
        self.is_token_in_cache = False
        self.token_should_be(self.reauthorized_token)

    def test_should_store_token_in_cache(self):
        self.is_token_in_cache = False
        self.token_should_be(self.reauthorized_token)
        assert_that(self.cache.tokens, is_not({}))

    def token_should_be(self, expected_token):
        if self.is_token_in_cache:
            self.cache.tokens['client'] = self.token
        oauth = OAuthStub('client', self.reauthorized_token)
        auth = CachedAuth(oauth, self.cache)
        assert_that(auth.authorize(), is_(expected_token))


class OAuthStub:
    def __init__(self, client, token):
        self.client = client
        self.token = token

    def authorize(self):
        return self.token

    def get_client(self):
        return self.client
