# -*- coding: utf-8 -*-
import unittest
from unittest_data_provider import data_provider
from tests.remote import given_client, should_return_error
from gopay import Language


class WhenApiFailedTest(unittest.TestCase):

    def test_status_of_non_existent_payment(self):
        gopay = given_client()
        non_existent_id = -10
        status = gopay.get_status(non_existent_id)
        should_return_error(status, 404)
