
from http import Browser
from api import GoPay,add_defaults
from oauth2 import OAuth2
from payments import Payments

def payments(config):
    config = add_defaults(config, {
        'scope': 'payment-all'
    })
    browser = Browser()
    gopay = GoPay(config, browser)
    auth = OAuth2(gopay)
    return Payments(gopay, auth)
