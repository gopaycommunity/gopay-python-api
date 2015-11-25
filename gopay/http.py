import unirest

def browse(url):
    try:
        method = 'get'
        u = getattr(unirest, method)(url)
        return Response(u.raw_body, u.body, u.code)
    except Exception as e:
        return Response(e, {}, 500)

class Response:
    def __init__(self, raw_body, json, status_code):
        self.raw_body = str(raw_body)
        self.json = json
        self.status_code = status_code
    def has_succeed(self):
        return self.status_code == 200
    def __str__(self):
        return self.raw_body
