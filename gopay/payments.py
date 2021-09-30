from typing import Dict, List, Union

from gopay.api import JSON, FORM, add_defaults, Response, GoPay
from gopay.oauth2 import OAuth2


paymentSessionId = Union[List[str], str]
number = Union[int, str]
class Payments:
    def __init__(self, gopay: GoPay, oauth: OAuth2) -> None:
        self.gopay = gopay
        self.oauth = oauth

    def create_payment(self, payment: Dict) -> Response:
        payment = add_defaults(payment, {
            'target': {
                'type': 'ACCOUNT',
                'goid': self.gopay.config['goid']
            },
            'lang': self.gopay.config['language']
        })
        return self._api('payments/payment', JSON, payment)

    def get_status(self, id_payment: Union[int, str]) -> Response:
        return self._api('payments/payment/' + str(id_payment), FORM, None)

    def refund_payment(self, id_payment: Union[int, str], amount: int) -> Response:
        return self._api('payments/payment/' + str(id_payment) + '/refund', FORM, {'amount': amount})

    def refund_payment_eet(self, id_payment: Union[int, str], payment_data: Dict) -> Response:
        return self._api('payments/payment/' + str(id_payment) + '/refund', JSON, payment_data)

    def create_recurrence(self, id_payment: Union[int, str], payment: Dict) -> Response:
        return self._api('payments/payment/' + str(id_payment) + '/create-recurrence', JSON, payment)

    def void_recurrence(self, id_payment: Union[int, str]) -> Response:
        return self._api('payments/payment/' + str(id_payment) + '/void-recurrence', FORM, {})

    def capture_authorization(self, id_payment: Union[int, str]) -> Response:
        return self._api('payments/payment/' + str(id_payment) + '/capture', FORM, {})

    def capture_authorization_partial(self, id_payment: Union[int, str], capture_payment: Dict) -> Response:
        return self._api('payments/payment/' + str(id_payment) + '/capture', JSON, capture_payment)

    def void_authorization(self, id_payment: Union[int, str]) -> Response:
        return self._api('payments/payment/' + str(id_payment) + '/void-authorization', FORM, {})

    def get_payment_instruments(self, go_id: Union[int, str], currency: str) -> Response:
        return self._api('eshops/eshop/' + go_id + '/payment-instruments/' + currency, '', None)

    def get_account_statement(self, account_statement: Dict) -> Response:
        return self._api('accounts/account-statement', JSON, account_statement)

    def get_eet_receipt_by_payment_id(self, id_payment: Union[int, str]) -> Response:
        return self._api('payments/payment/' + str(id_payment) + '/eet-receipts', JSON, None)

    def find_eet_receipts_by_filter(self, filter: Dict) -> Response:
        return self._api('eet-receipts', JSON, filter)

    def get_supercash_coupon_batch_status(self, batch_id: Union[int, str]) -> Response:
        return self._api('batch/' + str(batch_id), FORM, None)

    def get_supercash_coupon_batch(self, batch_id: Union[int, str]) -> Response:
        return self._api('supercash/coupon/find?batch_request_id=' + str(batch_id) + '&go_id='
                         + str(self.gopay.config['goid']), FORM, None)

    def find_supercash_coupons(self, paymentSessionId: paymentSessionId) -> Response:
        if type(paymentSessionId) is list:
            ids_string = ','.join(map(str, paymentSessionId))
        else:
            ids_string = str(paymentSessionId)
        return self._api('supercash/coupon/find?payment_session_id_list=' + ids_string + '&go_id='
                         + str(self.gopay.config['goid']), FORM, None)

    def get_supercash_coupon(self, coupon_id: Union[int, str]) -> Response:
        return self._api('supercash/coupon/' + str(coupon_id), FORM, None)

    def url_to_embedjs(self) -> str:
        return self.gopay.url('gp-gw/js/embed.js')

    def _api(self, url: str, content_type: str, data: dict) -> Response:
        token = self.oauth.authorize()
        if token.token:
            return self.gopay.call(url, content_type, 'Bearer ' + token.token, data)
        else:
            return token.response
