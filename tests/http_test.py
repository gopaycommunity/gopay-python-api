import unittest
from hamcrest import *
from unittest_data_provider import data_provider
from gopay.http import Browser, Request


class HttpTest(unittest.TestCase):
    urls = lambda: (
        ('http://www.rozpisyzapasu.cz/api/', True, "links", has_key('links')),
        ('http://www.non-existent-page.cz/', False, "Max retries exceeded with url", is_({}))
    )

    def setUp(self):
        self.args = None

    @data_provider(urls)
    def test_should_return_response(self, url, has_succeed, expected_response, expected_json):
        response = self.browse(url)
        assert_that(response.has_succeed(), is_(has_succeed))
        assert_that(str(response), contains_string(expected_response))
        assert_that(response.json, expected_json)

    def test_should_log_communication(self):
        self.browse('http://www.rozpisyzapasu.cz/api/')
        assert_that(self.args, has_length(2))

    def browse(self, url):
        request = Request()
        request.url = url
        browser = Browser(self.log_spy, 1)
        return browser.browse(request)

    def log_spy(self, *args):
        self.args = args
