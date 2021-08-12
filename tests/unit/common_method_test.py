import unittest
import gopay
from gopay.enums import Currency, StatementGeneratingFormat
from tests.unit.utils import Utils


class TestCommonMethods(unittest.TestCase):

    """ TestCommonMethods class
    
    To execute test for certain method properly it is necessary to add prefix 'test' to its name.
    
    """

    def setUp(self):
        self.payments = gopay.payments({
            'goid': Utils.GO_ID,
            'clientId': Utils.CLIENT_ID,
            'clientSecret': Utils.CLIENT_SECRET,
            'isProductionMode': False
        })

    def test_payment_status(self):
        payment_id = 3049525986
        response = self.payments.get_status(payment_id)

        if "error_code" not in str(response.json):
            print('Payment: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
            print('Payment gwUrl: ' + str(response.json['gw_url']))
            print('Payment state: ' + str(response.json['state']))
            print('Payment instrument: ' + ("NONE" if "'payment_instrument'" not in str(response.json) else str(response.json['payment_instrument'])))
            print('PreAuthorization: ' + ("NONE" if "'preauthorization'" not in str(response.json) else str(response.json['preauthorization'])))
            print('Recurrence: ' + ("NONE" if "'recurrence'" not in str(response.json) else str(response.json['recurrence'])))
        else:
            print('Error: ' + str(response.json))

    def test_payment_instrument_root(self):
        instruments_list = self.payments.get_payment_instruments(Utils.GO_ID, Currency.CZECH_CROWNS)

        if "error_code" not in str(instruments_list.json):
            print('List of enabled payments instruments: \n' + 'Groups: ' + str(instruments_list.json['groups']))
            print('---------------------------------------------------------------------------------------------------')
            print('Enabled payments instruments: ' + str(instruments_list.json['enabledPaymentInstruments']))
        else:
            print('Error: ' + str(instruments_list.json))

    def test_statement_generating(self):
        account_statement = {
            'date_from': '2017-01-01',
            'date_to': '2017-02-27',
            'goid': Utils.GO_ID,
            'currency': Currency.CZECH_CROWNS,
            'format': StatementGeneratingFormat.CSV_A,
        }

        statement = self.payments.get_account_statement(account_statement)

        if "error_code" not in str(statement.json):
            print('Content of array to string: \n' + str(statement.raw_body))
        else:
            print('Error: ' + str(statement.json))