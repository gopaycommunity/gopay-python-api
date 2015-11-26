
from base64 import b64encode
from api import FORM
from datetime import datetime,timedelta

class OAuth2:
    def __init__(self, gopay):
        self.gopay = gopay

    def authorize(self):
        token = AccessToken()
        token.response = self.gopay.call(
            'oauth2/token',
            FORM,
            'Basic ' + b64encode(self.gopay.config['clientId'] + ':' + self.gopay.config['clientSecret']),
            {
                'grant_type': 'client_credentials',
                'scope': self.gopay.config['scope']
            }
        )
        if token.response.has_succeed():
            token.token = token.response.json['access_token']
            token.expiration_date = datetime.now() + timedelta(seconds=token.response.json['expires_in'])
        return token


class AccessToken:
    def __init__(self):
        self.token = None
        self.response = None
        self.expiration_date = None

    def is_expired(self):
        return self.token is None
