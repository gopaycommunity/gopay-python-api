from gopay import Payments


class TestCreatePayment:
    def test_create_payment(self, payments: Payments, base_payment: dict):
        response = payments.create_payment(base_payment)
        response_body = response.json
        assert "error_code" not in response_body
