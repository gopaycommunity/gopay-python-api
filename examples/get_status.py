import gopay

payments = gopay.payments({
    'goid': 'my goid',
    'clientId': 'my id',
    'clientSecret': 'my secret',
    'isProductionMode': False,
    'scope': gopay.TokenScope.ALL,
    'language': gopay.Language.CZECH
})

response = payments.get_status('payment id')
if response.has_succeed():
    print "hooray, API returned " + str(response)
else:
    print "oops, API returned " + str(response.status_code) + ": " + str(response)
