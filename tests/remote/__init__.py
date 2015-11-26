from gopay import payments, add_defaults
from hamcrest import *
from test.test_support import EnvironmentVarGuard


def given_client(config=None):
    env = EnvironmentVarGuard()
    return payments(
        add_defaults(config, {
            'goid': env.get('goid'),
            'clientId': env.get('clientId'),
            'clientSecret': env.get('clientSecret'),
            'isProductionMode': False
        }),
        {
            'logger': debug_logger
        }
    )


def should_return(response, field, expected_value):
    assert_that(response.has_succeed(), is_(True))
    assert_that(response.status_code, is_(200))
    assert_that(response.json[field], expected_value)


def should_return_error(response, status_code, expected_error):
    assert_that(response.has_succeed(), is_(False))
    assert_that(response.status_code, is_(status_code))
    assert_that(response.json['errors'][0], is_(expected_error))


def debug_logger(request, response):
    print vars(request)
    print vars(response)
    print ""
