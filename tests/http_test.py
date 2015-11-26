import unittest
from hamcrest import *
from unittest_data_provider import data_provider
from gopay.http import Browser, Request

class HttpTest(unittest.TestCase):
    urls = lambda: (
        ('http://www.rozpisyzapasu.cz/api/', True, "links", is_not),
        ('http://www.non-existent-page.cz/', False, "urlopen error", is_)
    )

    @data_provider(urls)
    def test_should_return_response(self, url, has_succeed, expected_response, assert_json):
        request = Request()
        request.url = url
        response = Browser(1).browse(request)
        assert_that(response.has_succeed(), is_(has_succeed))
        assert_that(str(response), contains_string(expected_response))
        assert_that(response.json, assert_json({}))
