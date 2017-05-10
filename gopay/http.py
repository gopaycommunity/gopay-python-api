import requests


class Browser:
    def __init__(self, logger, timeout):
        self.logger = logger
        self.timeout = timeout

    def browse(self, request):
        try:
            r = requests.request(request.method, request.url, headers=request.headers, data=request.body, timeout=self.timeout)
            response = Response(r.content, r.json(), r.status_code)
        except ValueError as ve:
            response = Response(r.content, None, r.status_code)
        except Exception as e:
            response = Response(e, {}, 500)
        self.logger(request, response)
        return response


class Request:
    def __init__(self):
        self.method = 'get'
        self.url = ''
        self.headers = {}
        self.body = {}


class Response:
    def __init__(self, raw_body, json, status_code):
        self.raw_body = str(raw_body)
        self.json = json
        self.status_code = status_code

    def has_succeed(self):
        return self.status_code == 200

    def __str__(self):
        return self.raw_body


def null_logger(*args):
    pass
