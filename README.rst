GoPay's Python SDK for Payments REST API
========================================

|Build Status|

 Requirements
-------------

-  Python >= 2.6, Python 3
-  dependencies:
   ```requests`` <https://github.com/kennethreitz/requests>`__

 Installation
-------------

The simplest way to install SDK is to use
`PIP <https://docs.python.org/2.7/installing/>`__:

.. code:: bash

    pip install gopay

Basic usage
-----------

.. code:: python

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

Configuration
~~~~~~~~~~~~~

Required fields
^^^^^^^^^^^^^^^

+-----------------+------------+--------------+
| Required field  | Data type  | Documentatio |
|                 |            | n            |
+=================+============+==============+
| ``goid``        | string     | default      |
|                 |            | GoPay        |
|                 |            | account used |
|                 |            | in           |
|                 |            | ``create_pay |
|                 |            | ment``       |
|                 |            | if           |
|                 |            | ``target``   |
|                 |            | is not       |
|                 |            | specified    |
+-----------------+------------+--------------+
| ``clientId``    | string     | https://doc. |
|                 |            | gopay.com/en |
|                 |            | /?shell#oaut |
|                 |            | h            |
+-----------------+------------+--------------+
| ``clientSecret` | string     | https://doc. |
| `               |            | gopay.com/en |
|                 |            | /?shell#oaut |
|                 |            | h            |
+-----------------+------------+--------------+
| ``isProductionM | boolean    | `test or     |
| ode``           |            | production   |
|                 |            | environment? |
|                 |            |  <https://he |
|                 |            | lp.gopay.com |
|                 |            | /en/s/ey>`__ |
+-----------------+------------+--------------+

Optional fields
^^^^^^^^^^^^^^^

+-----------------+------------+----------------+----------------+
| Optional field  | Data type  | Default value  | Documentation  |
+=================+============+================+================+
| ``scope``       | string     | ```gopay.enums | https://doc.go |
|                 |            | .TokenScope.AL | pay.com/en/?sh |
|                 |            | L`` </gopay/en | ell#scope      |
|                 |            | ums.py>`__     |                |
+-----------------+------------+----------------+----------------+
| ``language``    | string     | ```gopay.enums | language used  |
|                 |            | .Language.ENGL | in             |
|                 |            | ISH`` </gopay/ | ``create_payme |
|                 |            | enums.py>`__   | nt``           |
|                 |            |                | if ``lang`` is |
|                 |            |                | not specified  |
|                 |            |                | + used for     |
|                 |            |                | `localization  |
|                 |            |                | of             |
|                 |            |                | errors <https: |
|                 |            |                | //doc.gopay.co |
|                 |            |                | m/en/?shell#re |
|                 |            |                | turn-errors>`_ |
|                 |            |                | _              |
+-----------------+------------+----------------+----------------+
| ``timeout``     | int        | 30             | Browser        |
|                 |            |                | timeout in     |
|                 |            |                | seconds        |
+-----------------+------------+----------------+----------------+

 Available methods
~~~~~~~~~~~~~~~~~~

+------+-------------+
| API  | SDK method  |
+======+=============+
| `Cre | ``payments. |
| ate  | create_paym |
| stan | ent({})``   |
| dard |             |
| paym |             |
| ent  |             |
| <htt |             |
| ps:/ |             |
| /doc |             |
| .gop |             |
| ay.c |             |
| om/e |             |
| n/#s |             |
| tand |             |
| ard- |             |
| paym |             |
| ent> |             |
| `__  |             |
+------+-------------+
| `Sta | ``payments. |
| tus  | get_status( |
| of   | id_payment) |
| the  | ``          |
| paym |             |
| ent  |             |
| <htt |             |
| ps:/ |             |
| /doc |             |
| .gop |             |
| ay.c |             |
| om/e |             |
| n/#s |             |
| tatu |             |
| s-of |             |
| -the |             |
| -pay |             |
| ment |             |
| >`__ |             |
+------+-------------+
| `Ref | ``payments. |
| und  | refund_paym |
| of   | ent(id_paym |
| the  | ent, $amoun |
| paym | t)``        |
| ent  |             |
| <htt |             |
| ps:/ |             |
| /doc |             |
| .gop |             |
| ay.c |             |
| om/e |             |
| n/#r |             |
| efun |             |
| d-of |             |
| -the |             |
| -pay |             |
| ment |             |
| -(ca |             |
| ncel |             |
| atio |             |
| n)>` |             |
| __   |             |
+------+-------------+
| `Cre | ``payments. |
| ate  | create_paym |
| recu | ent({})``   |
| rrin |             |
| g    |             |
| paym |             |
| ent  |             |
| <htt |             |
| ps:/ |             |
| /doc |             |
| .gop |             |
| ay.c |             |
| om/e |             |
| n/#r |             |
| ecur |             |
| ring |             |
| -pay |             |
| ment |             |
| >`__ |             |
+------+-------------+
| `Rec | ``payments. |
| urri | create_recu |
| ng   | rrence(id_p |
| paym | ayment, {}) |
| ent  | ``          |
| on   |             |
| dema |             |
| nd < |             |
| http |             |
| s:// |             |
| doc. |             |
| gopa |             |
| y.co |             |
| m/en |             |
| /#re |             |
| curr |             |
| ing- |             |
| paym |             |
| ent- |             |
| on-d |             |
| eman |             |
| d>`_ |             |
| _    |             |
+------+-------------+
| `Can | ``payments. |
| cell | void_recurr |
| atio | ence(id_pay |
| n    | ment)``     |
| of   |             |
| the  |             |
| recu |             |
| rrin |             |
| g    |             |
| paym |             |
| ent  |             |
| <htt |             |
| ps:/ |             |
| /doc |             |
| .gop |             |
| ay.c |             |
| om/e |             |
| n/#c |             |
| ance |             |
| llat |             |
| ion- |             |
| of-t |             |
| he-r |             |
| ecur |             |
| ring |             |
| -pay |             |
| ment |             |
| >`__ |             |
+------+-------------+
| `Cre | ``payments. |
| ate  | create_paym |
| pre- | ent({})``   |
| auth |             |
| oriz |             |
| ed   |             |
| paym |             |
| ent  |             |
| <htt |             |
| ps:/ |             |
| /doc |             |
| .gop |             |
| ay.c |             |
| om/e |             |
| n/#p |             |
| re-a |             |
| utho |             |
| rize |             |
| d-pa |             |
| ymen |             |
| t>`_ |             |
| _    |             |
+------+-------------+
| `Cha | ``payments. |
| rge  | capture_aut |
| of   | horization( |
| pre- | id_payment) |
| auth | ``          |
| oriz |             |
| ed   |             |
| paym |             |
| ent  |             |
| <htt |             |
| ps:/ |             |
| /doc |             |
| .gop |             |
| ay.c |             |
| om/e |             |
| n/#c |             |
| harg |             |
| e-of |             |
| -pre |             |
| -aut |             |
| hori |             |
| zed- |             |
| paym |             |
| ent> |             |
| `__  |             |
+------+-------------+
| `Can | ``payments. |
| cell | void_author |
| atio | ization(id_ |
| n    | payment)``  |
| of   |             |
| the  |             |
| pre- |             |
| auth |             |
| oriz |             |
| ed   |             |
| paym |             |
| ent  |             |
| <htt |             |
| ps:/ |             |
| /doc |             |
| .gop |             |
| ay.c |             |
| om/e |             |
| n/#c |             |
| ance |             |
| llat |             |
| ion- |             |
| of-t |             |
| he-p |             |
| re-a |             |
| utho |             |
| rize |             |
| d-pa |             |
| ymen |             |
| t>`_ |             |
| _    |             |
+------+-------------+

SDK response? Has my call succeed?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SDK returns wrapped API response. Every method returns
```gopay.http.response`` object </gopay/http.py>`__. Structure of
``json/__str__`` should be same as in
`documentation <https://doc.gopay.com/en>`__. SDK throws no exception.
Please create an issue if you catch one.

.. code:: python

    response = payments.create_payment({})
    if response.has_succeed():
        print("hooray, API returned " + str(response))
        return response.json['gw_url'] # url for initiation of gateway
    else:
        # errors format: https://doc.gopay.com/en/?shell#http-result-codes
        print("oops, API returned " + str(response.status_code) + ": " + str(response))

+---------+-------------+
| Method  | Description |
+=========+=============+
| ``respo | checks if   |
| nse.has | API returns |
| _succee | status code |
| d()``   | *200*       |
+---------+-------------+
| ``respo | decoded     |
| nse.jso | response,   |
| n``     | returned    |
|         | objects are |
|         | converted   |
|         | into        |
|         | associative |
|         | arrays      |
+---------+-------------+
| ``respo | HTTP status |
| nse.sta | code        |
| tus_cod |             |
| e``     |             |
+---------+-------------+
| ``respo | raw body    |
| nse.__s | from HTTP   |
| tr__()` | response    |
| `       |             |
+---------+-------------+

 Are required fields and allowed values validated?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**No.** API `validates
fields <https://doc.gopay.com/en/?shell#return-errors>`__ pretty
extensively so there is no need to duplicate validation in SDK. It would
only introduce new type of error. Or we would have to perfectly simulate
API error messages. That's why SDK just calls API which behavior is well
documented in `doc.gopay.com <https://doc.gopay.com/en>`__.

--------------

Advanced usage
--------------

Initiation of the payment gateway
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # create payment and pass url to template
    response = payments.create_payment({})
    if response.has_succeed():
        templateParameters = {
            'gatewayUrl': response.json['gw_url'],
            'embedJs': gopay.url_to_embedjs()
        }
        # render template

`Inline gateway <https://doc.gopay.com/en/#inline-option>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: jinja

    <form action="<%= $gatewayUrl %>" method="post" id="gopay-payment-button">
      <button name="pay" type="submit">Pay</button>
      <script type="text/javascript" src="<%= $embedJs %>"></script>
    </form>

`Redirect gateway <https://doc.gopay.com/en/#redirect-option>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: jinja

    <form action="<%= $gatewayUrl %>" method="post">
      <button name="pay" type="submit">Pay</button>
    </form>

`Asynchronous initialization using JavaScript <https://github.com/gopaycommunity/gopay-php-api/blob/master/examples/js-initialization.md>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enums (`Code lists <https://doc.gopay.com/en/#code-lists>`__)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of hardcoding bank codes string you can use predefined enums.
Check using enums in `create-payment
example </examples/create_payment.py>`__

+----------------------------------------+------------------------------------------------------------------------+
| Type                                   | Description                                                            |
+========================================+========================================================================+
| `Language </gopay/enums.py>`__         | Payment language, localization of error messages                       |
+----------------------------------------+------------------------------------------------------------------------+
| `Token scope </gopay/enums.py>`__      | Authorization scope for `OAuth2 <https://doc.gopay.com/en/#oauth>`__   |
+----------------------------------------+------------------------------------------------------------------------+
| `Payment enums </gopay/enums.py>`__    | Enums for creating payment                                             |
+----------------------------------------+------------------------------------------------------------------------+
| `Response enums </gopay/enums.py>`__   | Result of creating payment, executing payment operations               |
+----------------------------------------+------------------------------------------------------------------------+

Cache access token
~~~~~~~~~~~~~~~~~~

Access token expires after 30 minutes so it's expensive to use new token
for every request. Unfortunately it's default behavior of
```gopay.oauth2.InMemoryTokenCache`` </gopay/oauth2.py>`__. But you can
implement your cache and store tokens in Memcache, Redis, files, ...
It's up to you.

Your cache must implement template methods ``get_token`` and
``set_token``. Be aware that there are two
`scopes <https://doc.gopay.com/en/?shell#scope>`__ (``TokenScope``) and
SDK can be used for different clients (``clientId``,
``isProductionMode``). So ``client`` passed to methods is unique
identifier (``string``) that is built for current environment. Below you
can see example implementation of caching tokens in memory:

.. code:: python

    # register cache in optional service configuration
    payments = gopay.payments(
        {}, # your config
        {'cache': MyCache()}
    )

.. code:: python

    class MyCache:
        def __init__(self):
            self.tokens = {}

        def get_token(self, client):
            return self.tokens.get(client) # return None if token not exists

        def set_token(self, client, token):
            self.tokens[client] = token

Log HTTP communication
~~~~~~~~~~~~~~~~~~~~~~

You can log every request and response from communication with API.
Check available loggers below. Or you can implement your own logger,
just implement function that takes two arguments:
```gopay.http.request`` </gopay/http.py>`__ and
```gopay.http.response`` </gopay/http.py>`__.

.. code:: python

    # register logger in optional service configuration
    payments = gopay.payments(
        {}, # your config
        {'logger': my_logger}
    )

    def my_logger(request, response):
        print(vars(request))
        print(vars(response))

+--------------------------------------------------------------+-------------------------------------------------------------------+
| Available logger                                             | Description                                                       |
+==============================================================+===================================================================+
| `gopay.http.null\_logger </gopay/http.py>`__                 | Default logger which does nothing                                 |
+--------------------------------------------------------------+-------------------------------------------------------------------+
| `tests.remote.debug\_logger </tests/remote/__init__.py>`__   | Prints request and response in `remote tests <tests/remote/>`__   |
+--------------------------------------------------------------+-------------------------------------------------------------------+

Contributing
------------

Contributions from others would be very much appreciated! Send `pull
request <https://github.com/gopaycommunity/gopay-python-api/pulls>`__/
`issue <https://github.com/gopaycommunity/gopay-python-api/issues>`__.
Thanks!

License
-------

Copyright (c) 2015 GoPay.com. MIT Licensed, see
`LICENSE <https://github.com/gopaycommunity/gopay-python-api/blob/master/LICENSE>`__
for details.

.. |Build Status| image:: https://travis-ci.org/gopaycommunity/gopay-python-api.svg?branch=master
   :target: https://travis-ci.org/gopaycommunity/gopay-python-api
