import logging

from gopay import Payments
from gopay.enums import QrCodeFormat


class TestQrPayment:
    """
    Integration tests for the QR payment endpoint.

    Prerequisites:
      - Set the GOID, CLIENT_ID, CLIENT_SECRET and GATEWAY_URL environment variables.
      - The `payments` and `base_payment` fixtures are provided by conftest.py.
    """

    _payment_id: int | str

    def test_create_payment_for_qr(self, payments: Payments, base_payment: dict):
        """
        Creates a standard payment that will be used for subsequent QR payment tests.
        Stores the payment id on the class so the other tests can re-use it.
        """
        response = payments.create_payment(base_payment)
        assert response.success, f"Payment creation failed: {response.json}"

        body = response.json
        logging.info(f"Created payment: {body}")

        assert "errors" not in body
        assert "id" in body
        assert body["state"] == "CREATED"

        # Store the payment id for the other tests in this class
        TestQrPayment._payment_id = body["id"]

    def test_get_qr_payment_default_format(self, payments: Payments):
        """
        Calls GET /api/payments/payment/{id}/qr-payment without specifying format.
        Expects a successful response containing amount, currency and qr_code.
        """
        payment_id = TestQrPayment._payment_id
        response = payments.get_qr_payment(payment_id)

        logging.info(f"QR payment response (default format): {response.json}")
        assert response.success, f"QR payment request failed: {response.json}"

        body = response.json
        assert "errors" not in body
        assert "amount" in body
        assert "currency" in body
        assert "qr_code" in body

        # qr_code must contain at least one of the known QR types
        qr_code = body["qr_code"]
        assert any(
            key in qr_code for key in ("spayd", "paybysquare", "sepa", "mnb_qr")
        ), f"Unexpected qr_code structure: {qr_code}"

    def test_get_qr_payment_png_format(self, payments: Payments):
        """
        Calls GET /api/payments/payment/{id}/qr-payment?format=png.
        """
        payment_id = TestQrPayment._payment_id
        response = payments.get_qr_payment(payment_id, format=QrCodeFormat.PNG)

        logging.info(f"QR payment response (PNG): {response.json}")
        assert response.success, f"QR payment PNG request failed: {response.json}"

        body = response.json
        assert "errors" not in body
        assert "qr_code" in body

    def test_get_qr_payment_svg_format(self, payments: Payments):
        """
        Calls GET /api/payments/payment/{id}/qr-payment?format=svg.
        """
        payment_id = TestQrPayment._payment_id
        response = payments.get_qr_payment(payment_id, format=QrCodeFormat.SVG)

        logging.info(f"QR payment response (SVG): {response.json}")
        assert response.success, f"QR payment SVG request failed: {response.json}"

        body = response.json
        assert "errors" not in body
        assert "qr_code" in body

    def test_get_qr_payment_recipient_structure(self, payments: Payments):
        """
        Validates the structure of the recipient block in the QR payment response.
        """
        payment_id = TestQrPayment._payment_id
        response = payments.get_qr_payment(payment_id)
        assert response.success

        body = response.json
        assert "recipient" in body

        recipient = body["recipient"]
        # name is expected
        assert "name" in recipient

        # bank_account block (local + international) is expected
        if "bank_account" in recipient:
            bank_account = recipient["bank_account"]
            if "local" in bank_account:
                local = bank_account["local"]
                assert "account_number" in local
                assert "bank_code" in local
            if "international" in bank_account:
                international = bank_account["international"]
                assert "iban" in international
                # bic is not always present (depends on currency/payment type)
                assert any(
                    key in international for key in ("bic", "reference")
                ), f"Unexpected international bank_account structure: {international}"
