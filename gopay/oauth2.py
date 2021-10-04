from base64 import b64encode
from typing import Any
from gopay.api import FORM, GoPay
from datetime import datetime, timedelta

class AccessToken:
    def __init__(self) -> None:
        self.token = None
        self.response = None
        self.expiration_date = None

    def is_expired(self) -> bool:
        return self.token is None or not isinstance(self.expiration_date,
                                                    datetime) or self.expiration_date < datetime.now()
class OAuth2:
    def __init__(self, gopay: GoPay) -> None:
        self.gopay = gopay

    def authorize(self) -> AccessToken:
        credentials = self.gopay.config['clientId'] + ':' + self.gopay.config['clientSecret']
        token = AccessToken()
        token.response = self.gopay.call(
            '/oauth2/token',
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

    def get_client(self) -> str:
        return '-'.join([
            self.gopay.config['clientId'],
            'https://gw.sandbox.gopay.com/',
            self.gopay.config['scope']]
        )
class InMemoryTokenCache:
    def __init__(self):
        self.tokens = {}

    def get_token(self, client: str) -> AccessToken:
        return self.tokens.get(client)

    def set_token(self, client: str, token: AccessToken) -> None:
        self.tokens[client] = token

class CachedAuth:
    def __init__(self, oauth: OAuth2, cache: Any) -> None:
        self.oauth = oauth
        self.cache = cache

    def authorize(self) -> AccessToken:
        client = self.oauth.get_client()
        token = self.cache.get_token(client)
        if not isinstance(token, AccessToken) or token.is_expired():
            token = self.oauth.authorize()
            self.cache.set_token(client, token)
        return token


