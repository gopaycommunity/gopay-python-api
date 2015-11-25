
class OAuth2:
    def __init__(self, config):
        self.config = config

    def authorize(self):
        return AccessToken()

class AccessToken:
    def __init__(self, token=''):
        self.token = token
