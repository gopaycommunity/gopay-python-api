
from http import Request

class Payments:
    def __init__(self, browser, oauth):
        self.browser = browser
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
            request = Request()
            request.url = 'https://gw.sandbox.gopay.com/api/payments/payment' + url
            request.headers = {
                'Accept': 'application/json',
                'Content-Type':  content_type,
                'Authorization': 'Bearer ' + token.token
            }
            if (data is None):
                request.method = 'get'
            else:
                request.method = 'post'
                request.body = data
            return self.browser.browse(request)
        else:
            return token.response
