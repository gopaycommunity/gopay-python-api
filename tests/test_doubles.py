
from hamcrest import assert_that, is_

class GoPayMock:
    def __init__(self, config=None):
        self.request = ()
        self.config = config if config is not None else {}
        self.response = 'irrelevant browser response'

    def given_response(self, has_succeed=False, json = None):
        self.response = ResponseStub()
        self.response.result = has_succeed
        self.response.json = json

    def call(self, *args):
        self.request = args
        return self.response

    def url(self, url):
        return url

    def should_be_called_with(self, *args):
        assert_that(self.request, is_(args))


class ResponseStub:
    def __init__(self):
        self.result = False
        self.json = None

    def has_succeed(self):
        return self.result
