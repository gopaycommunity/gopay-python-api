import unittest
from hamcrest import *
from gopay.oauth2 import OAuth2, AccessToken

class OAuth2Test(unittest.TestCase):

    def test_should_return_access_token(self):
        oauth = OAuth2({
            'clientId': 'user',
            'clientSecret': 'pass',
            'scope': 'irrelevant scope'
        })
        token = oauth.authorize()
        assert_that(token, is_(instance_of(AccessToken)))
