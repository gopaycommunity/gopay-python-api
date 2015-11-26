from api import JSON, FORM, add_defaults


class Payments:
    def __init__(self, gopay, oauth):
        self.gopay = gopay
        self.oauth = oauth

    def create_payment(self, payment):
        payment = add_defaults(payment, {
            'target': {
                'type': 'ACCOUNT',
                'goid': self.gopay.config['goid']
            },
            'lang': self.gopay.config['language']
        })
        return self._api('', JSON, payment)

    def get_status(self, id_payment):
        return self._api('/' + str(id_payment), FORM, None)

    def refund_payment(self, id_payment, amount):
        return self._api('/' + str(id_payment) + '/refund', FORM, {'amount': amount})

    def create_recurrence(self, id_payment, payment):
        return self._api('/' + str(id_payment) + '/create-recurrence', JSON, payment)

    def void_recurrence(self, id_payment):
        return self._api('/' + str(id_payment) + '/void-recurrence', FORM, {})

    def capture_authorization(self, id_payment):
        return self._api('/' + str(id_payment) + '/capture', FORM, {})

    def void_authorization(self, id_payment):
        return self._api('/' + str(id_payment) + '/void-authorization', FORM, {})

    def url_to_embedjs(self):
        return self.gopay.url('gp-gw/js/embed.js')

    def _api(self, url, content_type, data):
        token = self.oauth.authorize()
        if token.token:
            return self.gopay.call('payments/payment' + url, content_type, 'Bearer ' + token.token, data)
        else:
            return token.response
