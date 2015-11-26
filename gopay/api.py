
from http import Request
import json

JSON = 'application/json'
FORM = 'application/x-www-form-urlencoded'

class GoPay:
    def __init__(self, config, browser):
        self.browser = browser
        self.config = config

    def url(self, path):
        host = 'https://gate.gopay.cz/' if self.config['isProductionMode'] else 'https://gw.sandbox.gopay.com/'
        return host + path

    def call(self, url, content_type, authorization, data):
        request = Request()
        request.url = self.url('api/' + url)
        request.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'cs-CZ' if self.config['language'] in ['CS', 'SK'] else 'en-US',
            'Content-Type':  content_type,
            'Authorization': authorization
        }
        if (data is None):
            request.method = 'get'
        else:
            request.method = 'post'
            request.body = json.dumps(data) if content_type == JSON else data
        return self.browser.browse(request)

def add_defaults(data, defaults):
    full = defaults.copy()
    full.update(data)
    return full
