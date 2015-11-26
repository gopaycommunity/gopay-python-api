
from http import Browser,null_logger
from api import GoPay,add_defaults
from oauth2 import OAuth2
from payments import Payments

def payments(config, services = {}):
    config = add_defaults(config, {
        'scope': 'payment-all',
        'timeout': 30
    })
    services = add_defaults(services, {
        'logger': null_logger
    })
    browser = Browser(services['logger'], config['timeout'])
    gopay = GoPay(config, browser)
    auth = OAuth2(gopay)
    return Payments(gopay, auth)
