from base64 import b64encode
from gopay.api import FORM
from datetime import datetime, timedelta


class OAuth2:
    def __init__(self, gopay):
        self.gopay = gopay

    def authorize(self):
        credentials = self.gopay.config['clientId'] + ':' + self.gopay.config['clientSecret']
        token = AccessToken()
        token.response = self.gopay.call(
            'oauth2/token',
            FORM,
            'Basic ' + b64encode(credentials.encode('utf-8')).decode('utf-8'),
            {
                'grant_type': 'client_credentials',
                'scope': self.gopay.config['scope']
            }
        )
        if token.response.has_succeed():
            token.token = token.response.json['access_token']
            token.expiration_date = datetime.now() + timedelta(seconds=token.response.json['expires_in'])
        return token

    def get_client(self):
        return '-'.join([
            self.gopay.config['clientId'],
            '1' if self.gopay.config['isProductionMode'] else '0',
            self.gopay.config['scope']]
        )


class AccessToken:
    def __init__(self):
        self.token = None
        self.response = None
        self.expiration_date = None

    def is_expired(self):
        return self.token is None or not isinstance(self.expiration_date,
                                                    datetime) or self.expiration_date < datetime.now()


class CachedAuth:
    def __init__(self, oauth, cache):
        self.oauth = oauth
        self.cache = cache

    def authorize(self):
        client = self.oauth.get_client()
        token = self.cache.get_token(client)
        if not isinstance(token, AccessToken) or token.is_expired():
            token = self.oauth.authorize()
            self.cache.set_token(client, token)
        return token


class InMemoryTokenCache:
    def __init__(self):
        self.tokens = {}

    def get_token(self, client):
        return self.tokens.get(client)

    def set_token(self, client, token):
        self.tokens[client] = token
