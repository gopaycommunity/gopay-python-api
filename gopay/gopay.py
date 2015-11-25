
from http import Request

class GoPay:
    def __init__(self, config, browser):
        self.browser = browser
        self.config = config

    def config(self, key):
        return self.config[key]

    def call(self, url, content_type, authorization, data):
        request = Request()
        request.url = 'https://gw.sandbox.gopay.com/api/' + url
        request.headers = {
            'Accept': 'application/json',
            'Content-Type':  content_type,
            'Authorization': authorization
        }
        if (data is None):
            request.method = 'get'
        else:
            request.method = 'post'
            request.body = data
        return self.browser.browse(request)
