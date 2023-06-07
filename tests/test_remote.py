from gopay import Payments
import logging
from gopay.enums import Currency, PaymentStatus


class TestRemote:
    def test_create_payment_and_get_status(
        self, payments: Payments, base_payment: dict
    ):
        response = payments.create_payment(base_payment)

        assert response.success
        response_body = response.json

        assert "gw_url" in response_body
        assert ".gopay." in response_body["gw_url"]

        assert "id" in response_body
        payment_id = response_body["id"]

        status_response = payments.get_status(payment_id)

        assert status_response.success
        status_body = status_response.json

        assert "state" in status_body
        assert status_body["state"] == "CREATED"

    def test_nonexistent_payment(self, payments: Payments):
        wrong_payment_id = -10
        response = payments.get_status(wrong_payment_id)

        assert not response.success
        assert response.status_code == 404
