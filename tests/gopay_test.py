import unittest
from hamcrest import *
from gopay import payments
from gopay.payments import Payments

class GoPayTest(unittest.TestCase):

    def test_should_build_payments(self):
        gopay = payments({
            'irrelevant config': 'irrelevant value'
        })
        assert_that(gopay, is_(instance_of(Payments)))
