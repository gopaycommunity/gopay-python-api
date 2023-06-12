import logging

from gopay import Payments
from gopay.enums import PaymentInstrument


class TestCards:
    def test_create_payment_with_card_token_request(
        self, payments: Payments, base_payment: dict
    ):
        base_payment["payer"].update(
            {
                "allowed_payment_instruments": [PaymentInstrument.PAYMENT_CARD],
                "request_card_token": True,
            }
        )

        response = payments.create_payment(base_payment)
        assert response.success
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" not in response_body
        assert "id" in response_body
        assert response_body["state"] == "CREATED"

    def test_create_payment_with_card_token(
        self, payments: Payments, base_payment: dict
    ):
        base_payment["payer"].update(
            {
                "allowed_payment_instruments": [PaymentInstrument.PAYMENT_CARD],
                "allowed_card_token": "X5GMEJIPGhRuIBm/Q5G+D6m0WYnjN70YoLFZhN61UeSu9U0TRrrx0T1Xxvqp2dUEwqBjy62stJFLzkMoRxfeoOfetEnJqotVYntw9BFEp3mbYwkTN7XsAU36MbMkYplwsPmXBeQD9XCYUfjXmn16WQ==",
            }
        )

        response = payments.create_payment(base_payment)
        assert response.success
        response_body = response.json
        logging.info(f"API Response: {response_body}")

        assert "errors" not in response_body
        assert "id" in response_body
        assert response_body["state"] == "CREATED"

    def test_active_card(self, payments: Payments):
        response = payments.get_card_details(3011475940)
        assert response.success
        response_body = response.json
        logging.info(response_body)
        assert response_body["status"] == "ACTIVE"

    def test_deleted_card(self, payments: Payments):
        response = payments.get_card_details(3011480505)
        assert response.success
        response_body = response.json
        logging.info(response_body)
        assert response_body["status"] == "DELETED"

    def test_delete_card(self, payments: Payments):
        response = payments.delete_card(3011480505)
        assert response.success
        assert response.status_code == 204
