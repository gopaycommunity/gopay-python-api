
from http import Request

class Payments:
    def __init__(self, browser):
        self.browser = browser

    def create_payment(self, payment):
        request = Request()
        request.url = 'https://gw.sandbox.gopay.com/api/payments/payment'
        request.method = 'post'
        request.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        request.body = payment
        return self.browser.browse(request)

    def get_status(self, id):
        request = Request()
        request.url = 'https://gw.sandbox.gopay.com/api/payments/payment/' + str(id)
        request.method = 'get'
        request.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return self.browser.browse(request)

