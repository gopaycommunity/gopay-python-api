from gopay import Payments
from gopay.enums import Currency, StatementGeneratingFormat
import logging
import csv
import io


class TestGopayAccount:
    def test_payment_instruments(self, payments: Payments, goid: str):
        response = payments.get_payment_instruments(goid, Currency.CZECH_CROWNS)
        assert response.has_succeed()
        response_body = response.json
        logging.info(response_body)

        assert "errors" not in response_body
        assert "enabledPaymentInstruments" in response_body

    def test_statement_generating(self, payments: Payments, goid: str):
        statement_request = {
            "date_from": "2023-01-02",
            "date_to": "2023-02-27",
            "goid": goid,
            "currency": Currency.CZECH_CROWNS,
            "format": StatementGeneratingFormat.CSV_A,
        }

        response = payments.get_account_statement(statement_request)
        assert response.has_succeed()

        statement = response.raw_body.decode("windows-1250")
        logging.info(statement)

        assert "errors" not in statement
