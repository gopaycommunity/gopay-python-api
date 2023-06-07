from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class Recurrence(StrEnum):
    DAILY = "DAY"
    WEEKLY = "WEEK"
    MONTHLY = "MONTH"
    ON_DEMAND = "ON_DEMAND"


class Currency(StrEnum):
    CZECH_CROWNS = "CZK"
    EUROS = "EUR"
    POLISH_ZLOTY = "PLN"
    HUNGARIAN_FORINT = "HUF"
    BRITISH_POUND = "GBP"
    US_DOLLAR = "USD"
    ROMANIAN_LEU = "RON"
    BULGARIAN_LEV = "BGN"


class TokenScope(StrEnum):
    CREATE_PAYMENT = "payment-create"
    ALL = "payment-all"


class Result(StrEnum):
    ACCEPTED = "ACCEPTED"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class PaymentStatus(StrEnum):
    CREATED = "CREATED"
    PAYMENT_METHOD_CHOSEN = "PAYMENT_METHOD_CHOSEN"
    PAID = "PAID"
    AUTHORIZED = "AUTHORIZED"
    CANCELED = "CANCELED"
    TIMEOUTED = "TIMEOUTED"
    REFUNDED = "REFUNDED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"


class Language(StrEnum):
    CZECH = "CS"
    ENGLISH = "EN"
    SLOVAK = "SK"
    GERMAN = "DE"
    RUSSIAN = "RU"
    POLISH = "PL"
    HUNGARIAN = "HU"
    FRENCH = "FR"
    ROMANIAN = "RO"
    BULGARIAN = "BG"
    CROATIAN = "HR"
    ITALIAN = "IT"
    SPANISH = "ES"
    UKRAINIAN = "UK"
    ESTONIAN = "EE"
    LITHUANIAN = "LT"
    LATVIAN = "LV"
    SLOVENIAN = "SI"
    PORTUGUESE = "PT"


class PaymentInstrument(StrEnum):
    PAYMENT_CARD = "PAYMENT_CARD"
    BANK_ACCOUNT = "BANK_ACCOUNT"
    PREMIUM_SMS = "PRSMS"
    MPAYMENT = "MPAYMENT"
    PAYSAFECARD = "PAYSAFECARD"
    SUPERCASH = "SUPERCASH"
    GOPAY = "GOPAY"
    PAYPAL = "PAYPAL"
    BITCOIN = "BITCOIN"
    GPAY = "GPAY"
    ACCOUNT = "ACCOUNT"
    APPLE_PAY = "APPLE_PAY"
    CLICK_TO_PAY = "CLICK_TO_PAY"


class StatementGeneratingFormat(StrEnum):
    XLS_A = "XLS_A"
    XLS_B = "XLS_B"
    XLS_C = "XLS_C"
    CSV_A = "CSV_A"
    CSV_B = "CSV_B"
    CSV_C = "CSV_C"
    CSV_D = "CSV_D"
    CSV_E = "CSV_E"
    ABO_A = "ABO_A"


class ItemType(StrEnum):
    ITEM = "ITEM"
    DISCOUNT = "DISCOUNT"
    DELIVERY = "DELIVERY"
    POSTAGE = "POSTAGE"


class EETReceiptState(StrEnum):
    CREATED = "CREATED"
    DELIVERY_FAILED = "DELIVERY_FAILED"
    DELIVERED = "DELIVERED"


class EETMode(StrEnum):
    AUTO = "AUTO"
    EET = "EET"


class BankSwiftCode(StrEnum):
    # CZ
    CESKA_SPORITELNA = "GIBACZPX"
    KOMERCNI_BANKA = "KOMBCZPP"
    CSOB = "CEKOCZPP"
    RAIFFEISENBANK = "RZBCCZPP"
    UNICREDIT_BANK_CZ = "BACXCZPP"
    MONETA_MONEY_BANK = "AGBACZPP"
    FIO_BANKA = "FIOBCZPP"
    MBANK = "BREXCZPP"
    AIRBANK = "AIRACZPP"
    ING_BANK = "INGBCZPP"
    OBERBANK = "OBKLCZ2X"
    VUB_PRAHA = "SUBACZPP"
    HELLO_BANK = "BPPFCZP1"
    CREDITAS = "CTASCZ22"
    MAX_BANKA = "EXPNCZPP"
    JT_BANKA = "JTBPCZPP"
    # SK
    TATRA_BANKA = "TATRSKBX"
    VSEOBECNA_VEROVA_BANKA_BANKA = "SUBASKBX"
    UNICREDIT_BANK_SK = "UNCRSKBX"
    SLOVENSKA_SPORITELNA = "GIBASKBX"
    CSOB_SK = "CEKOSKBX"
    POSTOVA_BANKA = "POBNSKBA"
    OTP_BANKA_SLOVENSKO = "OTPVSKBX"
    PRIMA_BANKA_SLOVENSKO = "KOMASK2X"
    CITIBANK_EUROPE = "CITISKBA"
    FIO_BANKA_SK = "FIOZSKBA"
    MBANK_SK = "BREXSKBX"
    ING_BANK_SK = "INGBSKBX"
    JT_BANKA_SK = "JTBPSKBA"
    OBERBANK_SK = "OBKLSKBA"
    PRIVATBANKA = "BSLOSK22"
    BKS_BANK = "BFKKSKBB"
    RAIFFEISENBANK_SK = "TATRSKBXXXX"
    KOMERCNI_BANKA_SK = "KOMBSKBA"
    # PL
    MBANK1 = "BREXPLPW"
    CITI_HANDLOWY = "CITIPLPX"
    IKO = "BPKOPLPW-IKO"
    INTELIGO = "BPKOPLPW-INTELIGO"
    PLUS_BANK = "IVSEPLPP"
    BANK_BPH_SA = "BPHKPLPK"
    TOYOTA_BANK = "TOBAPLPW"
    VOLKSWAGEN_BANK = "VOWAPLP1"
    SGB = "GBWCPLPP"
    POCZTOWY_BANK = "POCZPLP4"
    BGZ_BANK = "GOPZPLPW"
    IDEA = "IEEAPLPA"
    BPS = "POLUPLPR"
    GETIN_ONLINE = "GBGCPLPK-GIO"
    BLIK = "GBGCPLPK-BLIK"
    NOBLE_BANK = "GBGCPLPK-NOB"
    ORANGE = "BREXPLPW-OMB"
    BZ_WBK = "WBKPPLPP"
    RAIFFEISEN_BANK_POLSKA_SA = "RCBWPLPW"
    POWSZECHNA_KASA_OSZCZEDNOSCI_BANK_POLSKI_SA = "BPKOPLPW"
    ALIOR_BANK = "ALBPPLPW"
    ING_BANK_SLASKI = "INGBPLPW"
    PEKAO_SA = "PKOPPLPW"
    GETIN_ONLINE1 = "GBGCPLPK"
    BANK_MILLENNIUM = "BIGBPLPW"
    BANK_OCHRONY_SRODOWISKA = "EBOSPLPW"
    BNP_PARIBAS_POLSKA = "PPABPLPK"
    CREDIT_AGRICOLE = "AGRIPLPR"
    DEUTSCHE_BANK_POLSKA_SA = "DEUTPLPX"
    DNB_NORD = "DNBANOKK"
    E_SKOK = "NBPLPLPW"
    EUROBANK = "SOGEPLPW"
    POLSKI_BANK_PRZEDSIEBIORCZOSCI_SPOLKA_AKCYJNA = "PBPBPLPW"
    # Others
    SPECIAL = "OTHERS"


class RecurrenceState(StrEnum):
    REQUESTED = "REQUESTED"
    STARTED = "STARTED"
    STOPPED = "STOPPED"


class PreAuthState(StrEnum):
    REQUESTED = "REQUESTED"
    AUTHORIZED = "AUTHORIZED"
    CAPTURED = "CAPTURED"
    CANCELED = "CANCELED"


class PaymentSubStatus(StrEnum):
    _101 = "_101"
    _102 = "_102"
    _3001 = "_3001"
    _3002 = "_3002"
    _3003 = "_3003"
    _5001 = "_5001"
    _5002 = "_5002"
    _5003 = "_5003"
    _5004 = "_5004"
    _5005 = "_5005"
    _5006 = "_5006"
    _5007 = "_5007"
    _5008 = "_5008"
    _5009 = "_5009"
    _5010 = "_5010"
    _5011 = "_5011"
    _5012 = "_5012"
    _5013 = "_5013"
    _5014 = "_5014"
    _5015 = "_5015"
    _5016 = "_5016"
    _5017 = "_5017"
    _5018 = "_5018"
    _5019 = "_5019"
    _5020 = "_5020"
    _5021 = "_5021"
    _5022 = "_5022"
    _5023 = "_5023"
    _5024 = "_5024"
    _5025 = "_5025"
    _5026 = "_5026"
    _5027 = "_5027"
    _5028 = "_5028"
    _5029 = "_5029"
    _5030 = "_5030"
    _5031 = "_5031"
    _5033 = "_5033"
    _5035 = "_5035"
    _5036 = "_5036"
    _5037 = "_5037"
    _5038 = "_5038"
    _5039 = "_5039"
    _5040 = "_5040"
    _5041 = "_5041"
    _5042 = "_5042"
    _5043 = "_5043"
    _5044 = "_5044"
    _5045 = "_5045"
    _5046 = "_5046"
    _5047 = "_5047"
    _5048 = "_5048"
    _5049 = "_5049"
    _5050 = "_5050"
    _6001 = "_6001"
    _6002 = "_6002"
    _6003 = "_6003"
    _6004 = "_6004"
    _6005 = "_6005"
    _6501 = "_6501"
    _6502 = "_6502"
    _6504 = "_6504"


class ContentType(StrEnum):
    FORM = "application/x-www-form-urlencoded"
    JSON = "application/json"
