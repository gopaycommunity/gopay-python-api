from gopay import Payments
import logging


class TestPreauthorization:
    def test_create_preauthorized_payment(self, payments: Payments, base_payment: dict):
        base_payment.update({"preauthorization": True})

        response = payments.create_payment(base_payment)
        assert response.has_succeed()
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" not in response_body
        assert "id" in response_body
        assert response_body["state"] == "CREATED"
        assert response_body["preauthorization"]["state"] == "REQUESTED"

    def test_capture_authorization(self, payments: Payments):
        payment_id = 3192064499

        response = payments.capture_authorization(payment_id)
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" in response_body
        error_dict = response_body["errors"][0]
        assert error_dict["error_name"] == "PAYMENT_CAPTURE_DONE"

    def test_void_authorization(self, payments: Payments):
        payment_id = 3192064499

        response = payments.capture_authorization(payment_id)
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" in response_body
        error_dict = response_body["errors"][0]
        assert error_dict["error_name"] == "PAYMENT_CAPTURE_DONE"
