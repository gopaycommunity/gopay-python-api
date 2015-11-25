
from http import Request

class Payments:
    def __init__(self, browser):
        self.gopay = GoPay(browser)

    def create_payment(self, payment):
        return self.gopay.json_call('', payment)

    def get_status(self, id):
        return self.gopay.form_call('/' + str(id), None)

    def refund_payment(self, id, amount):
        return self.gopay.form_call('/' + str(id) + '/refund', {'amount': amount})

    def create_recurrence(self, id, payment):
        return self.gopay.json_call('/' + str(id) + '/create-recurrence', payment)

    def void_recurrence(self, id):
        return self.gopay.form_call('/' + str(id) + '/void-recurrence', {})

    def capture_authorization(self, id):
        return self.gopay.form_call('/' + str(id) + '/capture', {})

    def void_authorization(self, id):
        return self.gopay.form_call('/' + str(id) + '/void-authorization', {})

class GoPay:
    def __init__(self, browser):
        self.browser = browser

    def json_call(self, url, data):
        return self.call(url, 'application/json', data)

    def form_call(self, url, data):
        return self.call(url, 'application/x-www-form-urlencoded', data)

    def call(self, url, content_type, data):
        request = Request()
        request.url = 'https://gw.sandbox.gopay.com/api/payments/payment' + url
        request.headers = {
            'Accept': 'application/json',
            'Content-Type':  content_type
        }
        if (data is None):
            request.method = 'get'
        else:
            request.method = 'post'
            request.body = data
        return self.browser.browse(request)