
class Payments:
    def __init__(self, gopay, oauth):
        self.gopay = gopay
        self.oauth = oauth

    def create_payment(self, payment):
        return self._json_call('', payment)

    def get_status(self, id):
        return self._form_call('/' + str(id), None)

    def refund_payment(self, id, amount):
        return self._form_call('/' + str(id) + '/refund', {'amount': amount})

    def create_recurrence(self, id, payment):
        return self._json_call('/' + str(id) + '/create-recurrence', payment)

    def void_recurrence(self, id):
        return self._form_call('/' + str(id) + '/void-recurrence', {})

    def capture_authorization(self, id):
        return self._form_call('/' + str(id) + '/capture', {})

    def void_authorization(self, id):
        return self._form_call('/' + str(id) + '/void-authorization', {})

    def _json_call(self, url, data):
        return self._authorized_call(url, 'application/json', data)

    def _form_call(self, url, data):
        return self._authorized_call(url, 'application/x-www-form-urlencoded', data)

    def _authorized_call(self, url, content_type, data):
        token = self.oauth.authorize()
        if (token.token):
            return self.gopay.call('payments/payment' + url, content_type, 'Bearer ' + token.token, data)
        else:
            return token.response
