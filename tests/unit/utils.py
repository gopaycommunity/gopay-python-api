from gopay.enums import PaymentInstrument, BankSwiftCode, Currency, Language

class Utils:

    GO_ID = '8712700986'
    CLIENT_ID = '1689337452'
    CLIENT_SECRET = 'CKr7FyEE'

    CLIENT_ID_EET = "1365575992"
    CLIENT_SECRET_EET = "NUVsrv4W"
    GO_ID_EET = '8289213768'

    @staticmethod
    def create_base_payment():
        base_payment = {
            'payer': {
                'allowed_payment_instruments': [PaymentInstrument.BANK_ACCOUNT, PaymentInstrument.PAYMENT_CARD],
                'allowed_swifts': [BankSwiftCode.CESKA_SPORITELNA, BankSwiftCode.RAIFFEISENBANK],
                #'default_swift': BankSwiftCode.CESKA_SPORITELNA,
                #'default_payment_instrument': PaymentInstrument.BANK_ACCOUNT,
                'contact': {
                    'email': 'test.test@gopay.cz',
                },
            },
            'order_number': '6789',
            'amount': '1900',
            'currency': Currency.CZECH_CROWNS,
            'order_description': '6789Description',
            'lang': Language.CZECH,  # if lang is not specified, then default lang is used
            'additional_params': [
                {'name': 'AdditionalKey', 'value': 'AdditionalValue'}
            ],
            'items': [
                {'name': 'Item01', 'amount': '1900', 'count' : '1'},
            ],
            'callback': {
                'return_url': 'https://eshop123.cz/return',
                'notification_url': 'https://eshop123.cz/notify'
            },
        }
        return base_payment
