
from http import Browser,null_logger
from api import GoPay,add_defaults
from oauth2 import OAuth2,InMemoryTokenCache,CachedAuth
from payments import Payments
from enums import Language,TokenScope

def payments(config, services = {}):
    config = add_defaults(config, {
        'scope': TokenScope.ALL,
        'language': Language.ENGLISH,
        'timeout': 30
    })
    services = add_defaults(services, {
        'logger': null_logger,
        'cache': InMemoryTokenCache()
    })
    browser = Browser(services['logger'], config['timeout'])
    gopay = GoPay(config, browser)
    auth = CachedAuth(OAuth2(gopay), services['cache'])
    return Payments(gopay, auth)
