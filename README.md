
# GoPay's Python SDK for Payments REST API

[![Build Status](https://travis-ci.org/gopaycommunity/gopay-python-sdk.svg?branch=master)](https://travis-ci.org/gopaycommunity/gopay-python-sdk)

## Requirements

- Python >= 2.6
- libraries: `unirest` (works in Python 2.X)

## Installation

The simplest way to install SDK is to use [PIP](https://docs.python.org/2.7/installing/):

```bash
pip install gopay
```

## Basic usage

```python
import gopay

# minimal configuration
payments = gopay.payments({
    'goid': 'my goid',
    'clientId': 'my id',
    'clientSecret': 'my secret',
    'isProductionMode': False
})

# full configuration
payments = gopay.payments({
    'goid': 'my goid',
    'clientId': 'my id',
    'clientSecret': 'my secret',
    'isProductionMode': False,
    'scope': gopay.TokenScope.ALL,
    'language': gopay.Language.CZECH,
    'timeout': 30
})
```

### Configuration

#### Required fields

Required field | Data type | Documentation |
-------------- | --------- | ----------- |
`goid` | string | default GoPay account used in `create_payment` if `target` is not specified
`clientId` | string | https://doc.gopay.com/en/?shell#oauth |
`clientSecret` | string | https://doc.gopay.com/en/?shell#oauth |
`isProductionMode` | boolean | [test or production environment?](https://help.gopay.com/en/s/ey) |

#### Optional fields

Optional field | Data type | Default value | Documentation |
-------------- | --------- | ------------- | ------------- |
`scope` | string | [`gopay.enums.TokenScope.ALL`](/gopay/enums.py) | https://doc.gopay.com/en/?shell#scope |
`language` | string | [`gopay.enums.Language.ENGLISH`](/gopay/enums.py) | language used in `create_payment` if `lang` is not specified + used for [localization of errors](https://doc.gopay.com/en/?shell#return-errors)
`timeout` | int | 30 | Browser timeout in seconds |


### Available methods

API | SDK method |
--- | ---------- |
[Create standard payment](https://doc.gopay.com/en/#standard-payment) | `payments.create_payment({})` |
[Status of the payment](https://doc.gopay.com/en/#status-of-the-payment) | `payments.get_status(id_payment)` |
[Refund of the payment](https://doc.gopay.com/en/#refund-of-the-payment-(cancelation)) | `payments.refund_payment(id_payment, $amount)` |
[Create recurring payment](https://doc.gopay.com/en/#recurring-payment) | `payments.create_payment({})` |
[Recurring payment on demand](https://doc.gopay.com/en/#recurring-payment-on-demand) | `payments.create_recurrence(id_payment, {})` |
[Cancellation of the recurring payment](https://doc.gopay.com/en/#cancellation-of-the-recurring-payment) | `payments.void_recurrence(id_payment)` |
[Create pre-authorized payment](https://doc.gopay.com/en/#pre-authorized-payment) | `payments.create_payment({})` |
[Charge of pre-authorized payment](https://doc.gopay.com/en/#charge-of-pre-authorized-payment) | `payments.capture_authorization(id_payment)` |
[Cancellation of the pre-authorized payment](https://doc.gopay.com/en/#cancellation-of-the-pre-authorized-payment) | `payments.void_authorization(id_payment)` |

### SDK response? Has my call succeed?

SDK returns wrapped API response. Every method returns
[`gopay.http.response` object](/gopay/http.py). Structure of `json/__str__`
should be same as in [documentation](https://doc.gopay.com/en).
SDK throws no exception. Please create an issue if you catch one.

```python
response = payments.create_payment({})
if response.has_succeed():
    print "hooray, API returned " + str(response)
    return response.json['gw_url'] # url for initiation of gateway
else:
    # errors format: https://doc.gopay.com/en/?shell#http-result-codes
    print "oops, API returned " + str(response.status_code) + ": " + str(response)
```

Method | Description |
------ | ---------- |
`response.has_succeed()` | checks if API returns status code _200_ |
`response.json` | decoded response, returned objects are converted into associative arrays |
`response.status_code` | HTTP status code |
`response.__str__()` | raw body from HTTP response |

### Are required fields and allowed values validated?

**No.** API [validates fields](https://doc.gopay.com/en/?shell#return-errors) pretty extensively
so there is no need to duplicate validation in SDK. It would only introduce new type of error.
Or we would have to perfectly simulate API error messages. That's why SDK just calls API which
behavior is well documented in [doc.gopay.com](https://doc.gopay.com/en).

*****

## Advanced usage

### Initiation of the payment gateway

```python
# create payment and pass url to template
response = payments.create_payment({})
if response.has_succeed():
    templateParameters = {
        'gatewayUrl': response.json['gw_url'],
        'embedJs': gopay.url_to_embedjs()
    }
    # render template
```

#### [Inline gateway](https://doc.gopay.com/en/#inline-option)

```jinja
<form action="<%= $gatewayUrl %>" method="post" id="gopay-payment-button">
  <button name="pay" type="submit">Pay</button>
  <script type="text/javascript" src="<%= $embedJs %>"></script>
</form>
```

#### [Redirect gateway](https://doc.gopay.com/en/#redirect-option)

```jinja
<form action="<%= $gatewayUrl %>" method="post">
  <button name="pay" type="submit">Pay</button>
</form>
```

#### [Asynchronous initialization using JavaScript](https://github.com/gopaycommunity/gopay-php-api/blob/master/examples/js-initialization.md)

### Enums ([Code lists](https://doc.gopay.com/en/#code-lists))

Instead of hardcoding bank codes string you can use predefined enums.
Check using enums in  [create-payment example](/examples/create_payment.py)

Type | Description |
---- | ----------- |
[Language](/gopay/enums.py) | Payment language, localization of error messages |
[Token scope](/gopay/enums.py) | Authorization scope for [OAuth2](https://doc.gopay.com/en/#oauth) |
[Payment enums](/gopay/enums.py) | Enums for creating payment |
[Response enums](/gopay/enums.py) | Result of creating payment, executing payment operations |

### Cache access token

Access token expires after 30 minutes so it's expensive to use new token for every request.
Unfortunately it's default behavior of [`gopay.oauth2.InMemoryTokenCache`](/gopay/oauth2.py).
But you can implement your cache and store tokens in Memcache, Redis, files, ... It's up to you.

Your cache must implement template methods `get_token` and `set_token`.
Be aware that there are two [scopes](https://doc.gopay.com/en/?shell#scope) (`TokenScope`) and
SDK can be used for different clients (`clientId`, `isProductionMode`). So `client` passed to
methods is unique identifier (`string`) that is built for current environment.
Below you can see example implementation of caching tokens in memory:


```python
# register cache in optional service configuration
payments = gopay.payments(
    {}, # your config
    {'cache': MyCache()}
)
```

```python
class MyCache:
    def __init__(self):
        self.tokens = {}

    def get_token(self, client):
        return self.tokens.get(client) # return None if token not exists

    def set_token(self, client, token):
        self.tokens[client] = token
```

### Log HTTP communication

You can log every request and response from communication with API. Check available loggers below.
Or you can implement your own logger, just implement function that takes two arguments:
[`gopay.http.request`](/gopay/http.py) and [`gopay.http.response`](/gopay/http.py).

```python
# register logger in optional service configuration
payments = gopay.payments(
    {}, # your config
    {'logger': my_logger}
)

def my_logger(request, response):
    print vars(request)
    print vars(response)
```

Available logger | Description |
---------------- | ----------- |
[gopay.http.null_logger](/gopay/http.py) | Default logger which does nothing |
[tests.remote.debug_logger](/tests/remote/__init__.py) | Prints request and response in [remote tests](tests/remote/) |

## Contributing

Contributions from others would be very much appreciated! Send
[pull request](https://github.com/gopaycommunity/gopay-python-sdk/pulls)/
[issue](https://github.com/gopaycommunity/gopay-python-sdk/issues). Thanks!

## License

Copyright (c) 2015 GoPay.com. MIT Licensed,
see [LICENSE](/LICENSE) for details.
