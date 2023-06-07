
# GoPay's Python SDK for Payments REST API

[![Build Status](https://travis-ci.org/gopaycommunity/gopay-python-api.svg?branch=master)](https://travis-ci.org/gopaycommunity/gopay-python-api)

## Requirements

- Python >= 3.8.1
- dependencies:
  - [`requests`](https://github.com/kennethreitz/requests)
  - [`deprecated`](https://github.com/tantale/deprecated)

## Installation

The simplest way to install SDK is to use [PIP](https://docs.python.org/3/installing/):

```bash
pip install gopay
```

## Basic usage

```python
import gopay
from gopay.enums import TokenScope, Language

# minimal configuration
payments = gopay.payments({
    "goid": "{{YOUR-GOID}}",
    "client_id": "{{YOUR-CLIENT-ID}}",
    "client_secret": "{{YOUR-CLIENT-SECRET}}",
    "gateway_url": 'https://gw.sandbox.gopay.com/api'
})

# full configuration
payments = gopay.payments({
    "goid": "{{YOUR-GOID}}",
    "client_id": "{{YOUR-CLIENT-ID}}",
    "client_secret": "{{YOUR-CLIENT-SECRET}}",
    "gateway_url": 'https://gw.sandbox.gopay.com/api'
    "scope": TokenScope.ALL,
    "language": Language.CZECH
})

# Sandbox URL: https://gw.sandbox.gopay.com/api
# Production URL: https://gate.gopay.cz/api
```

### Configuration

#### Required fields

Required field | Data type | Documentation |
-------------- | --------- | ----------- |
`goid` | string | GoID assigned by GoPay (production or sandbox) |
`client_id` | string | Client ID assigned by GoPay (production or sandbox) |
`client_secret` | string | Client Secret assigned by GoPay (production or sandbox) |
`gateway_url` | string | URL of the environment - production or sandbox (see [Docs](https://doc.gopay.com)) |

#### Optional fields

Optional field | Data type | Default value | Documentation |
-------------- | --------- | ------------- | ------------- |
`scope` | string | [`gopay.enums.TokenScope.ALL`](gopay/enums.py) | <https://doc.gopay.com/#access-token> |
`language` | string | [`gopay.enums.Language.ENGLISH`](gopay/enums.py) | default language to use + [localization of errors](https://doc.gopay.com/#error)

### Available methods

API | SDK method |
--- | ---------- |
[Create a payment](https://doc.gopay.com#payment-creation) | `payments.create_payment(payment: dict)` |
[Get status of a payment](https://doc.gopay.com#payment-inquiry) | `payments.get_status(payment_id: str \| int)` |
[Refund a payment](https://doc.gopay.com#payment-refund) | `payments.refund_payment(payment_id: int \| str, amount: int)` |
[Create a recurring payment](https://doc.gopay.com#creating-a-recurrence) | `payments.create_recurrence(payment_id: int \| str, payment: dict)` |
[Cancel a recurring payment](https://doc.gopay.com#void-a-recurring-payment) | `payments.void_recurrence(payment_id: int \| str)` |
[Capture a preauthorized payment](https://doc.gopay.com#capturing-a-preauthorized-payment) | `payments.capture_authorization(payment_id: int \| str)` |
[Capture a preauthorized payment partially](https://doc.gopay.com#partially-capturing-a-preauthorized-payment) | `payments.capture_authorization_partial(payment_id: int \| str, payment: dict)` |
[Void a preauthorized payment](https://doc.gopay.com#voiding-a-preauthorized-payment) | `payments.void_authorization(payment_id: int \| str)` |
[Get payment card details](https://doc.gopay.com#payment-card-inquiry) | `payments.get_card_details(card_id: int \| str)` |
[Delete a saved card](https://doc.gopay.com#payment-card-deletion) | `payments.delete_card(card_id: int \| str)` |
[Get allowed payment methods for a currency](https://doc.gopay.com#available-payment-methods-for-a-currency) | `payments.get_payment_instruments(goid: int \| str, currency: gopay.enums.Currency)` |
[Get all allowed payment methods](https://doc.gopay.com#all-available-payment-methods) | `payments.get_payment_instruments_all(goid: int \| str)` |
[Generate an account statement](https://doc.gopay.com#account-statement) | `payments.get_account_statement(statement_request: dict)`

### SDK response? Has my call succeed?

SDK returns wrapped API response. Every method returns
[`gopay.http.Response` object](gopay/http.py). Structure of the `json`
should be same as in [documentation](https://doc.gopay.com).
SDK throws no exception. Please create an issue if you catch one.

```python
response = payments.create_payment(...)
if response.success:
    print(f"Hooray, API returned {response}")
    return response.json["gw_url"] # url for initiation of gateway
else:
    # errors format: https://doc.gopay.com#HTTP-result-codes
    print(f"Oops, API returned  {response.status_code}: {response}")
```

Property/Method | Description |
------ | ---------- |
`response.success` | Checks if API call was successful |
`response.json` | decoded response, returned objects are converted into a dictionary if possiblem |
`response.status_code` | HTTP status code |
`response.raw_body` | raw bytes of the reponse content

### Are required fields and allowed values validated?

**Not yet.** API [validates fields](https://doc.gopay.com/#error) pretty extensively
so there is no need to duplicate validation in SDK. That's why SDK just calls API which
behavior is well documented in [doc.gopay.com](https://doc.gopay.com).
In the future, we might use Pydantic for parsing and validation.

*****

## Advanced usage

### Initiation of the payment gateway

```python
# create payment and pass url to template (e.g. Flask, Django)
response = payments.create_payment(...)
if response.has_succeed():
    context = {
        'gateway_url': response.json['gw_url'],
        'embedjs_url': payments.get_embedjs_url
    }
    # render template
```

#### [Inline gateway](https://doc.gopay.com#inline)

```jinja
<form action="{{ gateway_url }}" method="post" id="gopay-payment-button">
  <button name="pay" type="submit">Pay</button>
  <script type="text/javascript" src="{{ embedjs_url }}"></script>
</form>
```

#### [Redirect gateway](https://doc.gopay.com#redirect)

```jinja
<form action="{{ gateway_url }}" method="post">
  <button name="pay" type="submit">Pay</button>
</form>
```

#### [Asynchronous initialization using JavaScript](https://doc.gopay.com#inline)

### [Enums](https://doc.gopay.com#enums)

Instead of hardcoding bank codes string you can use predefined enums.
Check using enums in  [create-payment example](/examples/create_payment.py)

Type | Description |
---- | ----------- |
[Language](/gopay/enums.py) | Payment language, localization of error messages |
[Token scope](/gopay/enums.py) | Authorization scope for [OAuth2](https://doc.gopay.com/en/#oauth) |
[Payment enums](/gopay/enums.py) | Enums for creating payment |
[Response enums](/gopay/enums.py) | Result of creating payment, executing payment operations |

### Cache access token

Access token expires after 30 minutes it's expensive to use new token for every request.
By default, tokens are stored in memory [`gopay.services.DefaultCache`](/gopay/services.py) so they are reused as long as the object exists.
But you can implement your cache and store tokens in Memcache, Redis, files, ... It's up to you.

Your cache should inherit from [`gopay.services.AbstractCache`](/gopay/services.py) and implement its methods `get_token` and `set_token`.
Be aware that there are two [scopes](https://doc.gopay.com/#access-token) (`TokenScope`) and
SDK can be used for different clients (`client_id`, `gateway_url`). So `key` passed to methods is unique identifier (`str`) that is built for current environment.
Below you can see example implementation of caching tokens in memory:

```python
from gopay.services import AbstractCache
from gopay.http import AccessToken

class MyCache(AbstractCache):
    def __init__(self):
        self.tokens: dict[str, AccessToken] = {}

    def get_token(self, key: str) -> AccessToken | None:
        return self.tokens.get(key) # return None if token doesn't exist

    def set_token(self, key: str, token: AccessToken) -> None:
        self.tokens[key] = token

# register cache in optional service configuration
payments = gopay.payments(
    {...}, # your config
    {"cache": MyCache()}
)
```

### Log HTTP communication

You can log every request and response from communication with API. Check available loggers below.
Or you can implement your own logger, just implement function that matches the following signature:

```python
def logger(gopay.http.Request, gopay.http.Response) -> Any: ...
# or
Callable[[gopay.http.Response, gopay.http.Request], Any]
```

For example:

```python
from gopay.http import Request, Response

def my_logger(request: Request, response: Response) -> None:
    print(vars(request))
    print(vars(response))

# register logger in optional service configuration
payments = gopay.payments(
    {...}, # your config
    {"logger": my_logger}
)
```

The default logger uses `logging.debug` to log the responses and requests.

## Contributing

Contributions from others would be very much appreciated! Send
[pull request](https://github.com/gopaycommunity/gopay-python-api/pulls)/
[issue](https://github.com/gopaycommunity/gopay-python-api/issues). Thanks!

## License

Copyright (c) 2023 GoPay.com. MIT Licensed,
see [LICENSE](https://github.com/gopaycommunity/gopay-python-api/blob/master/LICENSE) for details.
