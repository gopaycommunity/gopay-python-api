
class TokenScope:
    CREATE_PAYMENT = 'payment-create'
    ALL = 'payment-all'

class Language:
    CZECH = 'CS'
    ENGLISH = 'EN'
    SLOVAK = 'SK'
    GERMAN = 'DE'
    RUSSIAN = 'RU'

class Currency:
    CZECH_CROWNS = 'CZK'
    EUROS = 'EUR'

class Recurrence:
    DAILY = 'DAY'
    WEEKLY = 'WEEK'
    MONTHLY = 'MONTH'
    ON_DEMAND = 'ON_DEMAND'

class PaymentInstrument:
    PAYMENT_CARD = 'PAYMENT_CARD'
    BANK_ACCOUNT = 'BANK_ACCOUNT'
    PREMIUM_SMS = 'PRSMS'
    MPAYMENT = 'MPAYMENT'
    PAYSAFECARD = 'PAYSAFECARD'
    SUPERCASH = 'SUPERCASH'
    GOPAY = 'GOPAY'
    PAYPAL = 'PAYPAL'

class BankSwiftCode:
    CESKA_SPORITELNA = 'GIBACZPX'
    KOMERCNI_BANKA = 'KOMBCZPP'
    RAIFFEISENBANK = 'RZBCCZPP'
    MBANK = 'BREXCZPP'
    FIO_BANKA = 'FIOBCZPP'
    CSOB = 'CEKOCZPP'
    ERA = 'CEKOCZPP-ERA'
    VSEOBECNA_VEROVA_BANKA_BANKA = 'SUBASKBX'
    TATRA_BANKA = 'TATRSKBX'
    UNICREDIT_BANK_SK = 'UNCRSKBX'
    SLOVENSKA_SPORITELNA = 'GIBASKBX'
    OTP_BANKA = 'OTPVSKBX'
    POSTOVA_BANKA = 'POBNSKBA'
    CSOB_SK = 'CEKOSKBX'
    SBERBANK_SLOVENSKO = 'LUBASKBX'

class PaymentStatus:
    CREATED = 'CREATED'
    PAYMENT_METHOD_CHOSEN = 'PAYMENT_METHOD_CHOSEN'
    PAID = 'PAID'
    AUTHORIZED = 'AUTHORIZED'
    CANCELED = 'CANCELED'
    TIMEOUTED = 'TIMEOUTED'
    REFUNDED = 'REFUNDED'
    PARTIALLY_REFUNDED = 'PARTIALLY_REFUNDED'

class Result:
    ACCEPTED = 'ACCEPTED'
    FINISHED = 'FINISHED'
    FAILED = 'FAILED'

# recurrence_state - https://doc.gopay.com/en/?php#additional_params
# preauthorization.state - https://doc.gopay.com/en/?php#pre-authorized-payment
class State:
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    STOPPED = 'STOPPED'

