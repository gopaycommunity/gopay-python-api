import logging

from gopay import Payments


class TestPayments:
    def test_create_payment(self, payments: Payments, base_payment: dict):
        response = payments.create_payment(base_payment)
        assert response.success
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" not in response_body
        assert "id" in response_body
        assert response_body["state"] == "CREATED"

    def test_refund_payment(self, payments: Payments):
        payment_id = 3178283550

        response = payments.refund_payment(payment_id, 1900)
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" in response_body
        error_dict = response_body["errors"][0]
        assert error_dict["error_name"] == "PAYMENT_REFUND_NOT_SUPPORTED"

    def test_payment_status(self, payments: Payments):
        payment_id = 3178283550

        response = payments.get_status(payment_id)
        assert response.success
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" not in response_body
        assert response_body["id"] == payment_id
        assert response_body["state"] == "REFUNDED"

    def test_history_refunds(self, payments: Payments):
        response = payments.get_history_of_refunds(3178283550)
        assert response.success
        response_body = response.json
        logging.info(response_body)

        assert "errors" not in response_body