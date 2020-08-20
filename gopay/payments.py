from gopay.api import JSON, FORM, add_defaults
from deprecated import deprecated

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
        return self._api('payments/payment', JSON, payment)

    def get_status(self, id_payment):
        return self._api('payments/payment/' + str(id_payment), FORM, None)

    def refund_payment(self, id_payment, amount):
        return self._api('payments/payment/' + str(id_payment) + '/refund', FORM, {'amount': amount})

    def refund_payment_eet(self, id_payment, payment_data):
        return self._api('payments/payment/' + str(id_payment) + '/refund', JSON, payment_data)

    def create_recurrence(self, id_payment, payment):
        return self._api('payments/payment/' + str(id_payment) + '/create-recurrence', JSON, payment)

    def void_recurrence(self, id_payment):
        return self._api('payments/payment/' + str(id_payment) + '/void-recurrence', FORM, {})

    def capture_authorization(self, id_payment):
        return self._api('payments/payment/' + str(id_payment) + '/capture', FORM, {})

    def capture_authorization_partial(self, id_payment, capture_payment):
        return self._api('payments/payment/' + str(id_payment) + '/capture', JSON, capture_payment)

    def void_authorization(self, id_payment):
        return self._api('payments/payment/' + str(id_payment) + '/void-authorization', FORM, {})

    def get_payment_instruments(self, go_id, currency):
        return self._api('eshops/eshop/' + str(go_id) + '/payment-instruments/' + str(currency), '', None)

    def get_account_statement(self, account_statement):
        return self._api('accounts/account-statement', JSON, account_statement)

    def get_eet_receipt_by_payment_id(self, id_payment):
        return self._api('payments/payment/' + str(id_payment) + '/eet-receipts', JSON, None)

    def find_eet_receipts_by_filter(self, filter):
        return self._api('eet-receipts', JSON, filter)

    @deprecated(version="1.2.4", reason="Payment Method Supercash is no longer supported")
    def create_supercash_coupon(self, base_coupon):
        base_coupon.update({'go_id': self.gopay.config['goid']})
        return self._api('supercash/coupon', JSON, base_coupon)

    @deprecated(version="1.2.4", reason="Payment Method Supercash is no longer supported")
    def create_supercash_batch(self, base_batch):
        base_batch.update({'go_id': self.gopay.config['goid']})
        return self._api('supercash/coupon/batch', JSON, base_batch)

    def get_supercash_coupon_batch_status(self, batch_id):
        return self._api('batch/' + str(batch_id), FORM, None)

    def get_supercash_coupon_batch(self, batch_id):
        return self._api('supercash/coupon/find?batch_request_id=' + str(batch_id) + '&go_id='
                         + str(self.gopay.config['goid']), FORM, None)

    def find_supercash_coupons(self, paymentSessionId):
        if type(paymentSessionId) is list:
            ids_string = ','.join(map(str, paymentSessionId))
        else:
            ids_string = str(paymentSessionId)
        return self._api('supercash/coupon/find?payment_session_id_list=' + ids_string + '&go_id='
                         + str(self.gopay.config['goid']), FORM, None)

    def get_supercash_coupon(self, coupon_id):
        return self._api('supercash/coupon/' + str(coupon_id), FORM, None)

    def url_to_embedjs(self):
        return self.gopay.url('gp-gw/js/embed.js')

    def _api(self, url, content_type, data):
        token = self.oauth.authorize()
        if token.token:
            return self.gopay.call(url, content_type, 'Bearer ' + token.token, data)
        else:
            return token.response
