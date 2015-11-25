
from base64 import b64encode

class OAuth2:
    def __init__(self, gopay):
        self.gopay = gopay

    def authorize(self):
        token = AccessToken()
        token.response = self.gopay.call(
            'oauth2/token',
            'application/x-www-form-urlencoded',
            'Basic ' + b64encode(self.gopay.config['clientId'] + ':' + self.gopay.config['clientSecret']),
            {
                'grant_type': 'client_credentials',
                'scope': self.gopay.config['scope']
            }
        )
        if token.response.has_succeed():
            token.token = token.response.json['access_token']
        return token


class AccessToken:
    def __init__(self):
        self.token = None
        self.response = None

    def is_expired(self):
        return self.token is None
