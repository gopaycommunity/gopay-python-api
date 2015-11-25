
from http import Request

class OAuth2:
    def __init__(self, config, browser):
        self.config = config
        self.browser = browser

    def authorize(self):
        request = Request()
        request.url = 'https://gw.sandbox.gopay.com/api/oauth2/token'
        request.method = 'post'
        request.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': self.config['clientId'] + ':' + self.config['clientSecret']
        }
        request.body = {
            'grant_type': 'client_credentials',
            'scope': self.config['scope']
        }
        token = AccessToken()
        token.response = self.browser.browse(request)
        if (token.response.has_succeed()):
            token.token = token.response.json['access_token']
        return token

class AccessToken:
    def __init__(self):
        self.token = None
        self.response = None

    def is_expired(self):
        return self.token is None
