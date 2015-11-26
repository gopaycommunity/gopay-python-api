
from http import Browser,null_logger
from api import GoPay,add_defaults
from oauth2 import OAuth2
from payments import Payments
from enums import Language,TokenScope

def payments(config, services = {}):
    config = add_defaults(config, {
        'scope': TokenScope.ALL,
        'language': Language.ENGLISH,
        'timeout': 30
    })
    services = add_defaults(services, {
        'logger': null_logger
    })
    browser = Browser(services['logger'], config['timeout'])
    gopay = GoPay(config, browser)
    auth = OAuth2(gopay)
    return Payments(gopay, auth)
