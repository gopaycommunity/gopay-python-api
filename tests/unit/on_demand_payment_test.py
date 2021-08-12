import unittest
import gopay
from tests.unit.utils import Utils
from gopay.enums import Recurrence


class TestOnDemandPayment(unittest.TestCase):

    """ TestOnDemandPayment class
    
    To execute test for certain method properly it is necessary to add prefix 'test' to its name.
    
    """

    def setUp(self):
        self.payments = gopay.payments({
            'goid': Utils.GO_ID,
            'clientId': Utils.CLIENT_ID,
            'clientSecret': Utils.CLIENT_SECRET,
            'isProductionMode': False
        })

    def _create_on_demand_payment(self):
        base_payment = Utils.create_base_payment()

        base_payment.update({'recurrence': {
            'recurrence_cycle': Recurrence.ON_DEMAND,
            'recurrence_date_to': '2018-04-01'
        }})

        response = self.payments.create_payment(base_payment)

        if "error_code" not in str(response.json):
            print('Payment: ' + str(response.json))
            print('Payment id: ' + str(response.json['id']))
            print('Payment gwUrl: ' + str(response.json['gw_url']))
            print('Payment instrument: ' + ("NONE" if "'payment_instrument'" not in str(response.json) else str(response.json['payment_instrument'])))
            print('Recurrence: ' + ("NONE" if "'recurrence'" not in str(response.json) else str(response.json['recurrence'])))
        else:
            print('Error: ' + str(response.json))

    def test_create_next_on_demand_payment(self):
        next_payment = {
            'amount': '4000',
            'currency': 'CZK',
            'order_number': 'OnDemand6789',
            'order_description': 'OnDemand6789Description',
            'items': [
                {'name': 'item01', 'amount': '2000', 'count' : '1'},
            ],
        }

        on_demand_payment = self.payments.create_recurrence(3049520708, next_payment)

        if "error_code" not in str(on_demand_payment.json):
            print('Payment: ' + str(on_demand_payment.json))
            print('Payment id: ' + str(on_demand_payment.json['id']))
            print('Payment gwUrl: ' + str(on_demand_payment.json['gw_url']))
            print('Payment instrument: ' + ("NONE" if "'payment_instrument'" not in str(on_demand_payment.json) else str(on_demand_payment.json['payment_instrument'])))
            print('Recurrence: ' + ("NONE" if "'recurrence'" not in str(on_demand_payment.json) else str(on_demand_payment.json['recurrence'])))
        else:
            print('Error: ' + str(on_demand_payment.json))
