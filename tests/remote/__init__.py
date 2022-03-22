from gopay import payments, add_defaults
from hamcrest import *
import sys

from tests.unit.utils import Utils


def given_client(config=None):
    return payments(
        add_defaults(
            config,
            {
                "goid": Utils.GO_ID,
                "clientId": Utils.CLIENT_ID,
                "clientSecret": Utils.CLIENT_SECRET,
                "gatewayUrl": Utils.GATEWAY_URL,
            },
        ),
        {"logger": debug_logger},
    )


def should_return(response, field, expected_value):
    assert_that(response.has_succeed(), is_(True))
    assert_that(response.status_code, is_(200))
    assert_that(response.json[field], expected_value)


def should_return_error(response, status_code):
    assert_that(response.has_succeed(), is_(False))
    assert_that(response.status_code, is_(status_code))


def debug_logger(request, response):
    print(vars(request))
    print(vars(response))
    print("")
