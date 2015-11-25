
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
        response = self.browser.browse(request)
        return AccessToken()

class AccessToken:
    def __init__(self, token=''):
        self.token = token
