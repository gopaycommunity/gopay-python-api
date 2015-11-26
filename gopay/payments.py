
from gopay import JSON,FORM

class Payments:
    def __init__(self, gopay, oauth):
        self.gopay = gopay
        self.oauth = oauth

    def create_payment(self, payment):
        return self._api('', JSON, payment)

    def get_status(self, id):
        return self._api('/' + str(id), FORM, None)

    def refund_payment(self, id, amount):
        return self._api('/' + str(id) + '/refund', FORM, {'amount': amount})

    def create_recurrence(self, id, payment):
        return self._api('/' + str(id) + '/create-recurrence', JSON, payment)

    def void_recurrence(self, id):
        return self._api('/' + str(id) + '/void-recurrence', FORM, {})

    def capture_authorization(self, id):
        return self._api('/' + str(id) + '/capture', FORM, {})

    def void_authorization(self, id):
        return self._api('/' + str(id) + '/void-authorization', FORM, {})

    def _api(self, url, content_type, data):
        token = self.oauth.authorize()
        if (token.token):
            return self.gopay.call('payments/payment' + url, content_type, 'Bearer ' + token.token, data)
        else:
            return token.response
