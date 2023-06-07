from gopay import Payments
from gopay.enums import Recurrence
import logging


class TestRecurrence:
    def test_create_autp_recurrent_payment(
        self, payments: Payments, base_payment: dict
    ):
        base_payment.update(
            {
                "recurrence": {
                    "recurrence_cycle": Recurrence.WEEKLY,
                    "recurrence_period": 1,
                    "recurrence_date_to": "2099-12-31",
                }
            }
        )

        response = payments.create_payment(base_payment)
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" not in response_body
        assert "id" in response_body
        assert response_body["state"] == "CREATED"
        assert response_body["recurrence"]["recurrence_cycle"] == Recurrence.WEEKLY
        assert response_body["recurrence"]["recurrence_state"] == "REQUESTED"

    def create_ondemand_recurrent_payment(self, payments: Payments, base_payment: dict):
        base_payment.update(
            {
                "recurrence": {
                    "recurrence_cycle": Recurrence.ON_DEMAND,
                    "recurrence_date_to": "2099-12-31",
                }
            }
        )

        response = payments.create_payment(base_payment)
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" not in response_body
        assert "id" in response_body
        assert response_body["state"] == "CREATED"
        assert response_body["recurrence"]["recurrence_cycle"] == Recurrence.ON_DEMAND
        assert response_body["recurrence"]["recurrence_state"] == "REQUESTED"

    def test_void_recurrence(self, payments: Payments):
        payment_id = 3049520773

        response = payments.void_recurrence(payment_id)
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" in response_body
        error_dict = response_body["errors"][0]
        assert error_dict["error_name"] == "PAYMENT_RECURRENCE_STOPPED"

    def test_create_next_ondemand_payment(self, payments: Payments):
        payment_id = 3049520708
        next_payment = {
            "amount": "4000",
            "currency": "CZK",
            "order_number": "OnDemand6789",
            "order_description": "OnDemand6789Description",
            "items": [
                {"name": "item01", "amount": "2000", "count": "1"},
            ],
        }

        response = payments.create_recurrence(payment_id, next_payment)
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" in response_body
        error_dict = response_body["errors"][0]
        assert error_dict["error_name"] == "PAYMENT_RECURRENCE_STOPPED"
