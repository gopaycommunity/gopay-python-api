from __future__ import annotations

from dataclasses import dataclass

from gopay.api import GoPay, Response
from gopay.enums import ContentType, Currency


@dataclass
class Payments:
    """
    Handles the API calls. Maps inidividual API Calls to Python methods and adds some
    defaults
    """

    gopay: GoPay

    def create_payment(self, payment: dict) -> Response:
        """
        https://doc.gopay.com#payment-creation
        """

        # Add defaults for goid and lang if not present
        if "target" not in payment:
            payment.update(
                {"target": {"type": "ACCOUNT", "goid": self.gopay.config["goid"]}}
            )
        if "lang" not in payment:
            payment.update({"lang": self.gopay.config["language"]})
        return self.gopay.call("POST", "/payments/payment", ContentType.JSON, payment)

    def get_status(self, payment_id: str | int) -> Response:
        """
        https://doc.gopay.com#payment-inquiry
        """
        return self.gopay.call("GET", f"/payments/payment/{payment_id}")

    def refund_payment(self, payment_id: int | str, amount: int) -> Response:
        """
        https://doc.gopay.com#payment-refund
        """
        return self.gopay.call(
            "POST",
            f"/payments/payment/{payment_id}/refund",
            ContentType.FORM,
            {"amount": amount},
        )

    def create_recurrence(self, payment_id: int | str, payment: dict) -> Response:
        """
        https://doc.gopay.com#creating-a-recurrence
        """
        return self.gopay.call(
            "POST",
            f"/payments/payment/{payment_id}/create-recurrence",
            ContentType.JSON,
            payment,
        )

    def void_recurrence(self, payment_id: int | str) -> Response:
        """
        https://doc.gopay.com#void-a-recurring-payment
        """
        return self.gopay.call(
            "POST", f"/payments/payment/{payment_id}/void-recurrence"
        )

    def capture_authorization(self, payment_id: int | str) -> Response:
        """
        https://doc.gopay.com#capturing-a-preauthorized-payment
        """
        return self.gopay.call("post", f"/payments/payment/{payment_id}/capture")

    def capture_authorization_partial(
        self, payment_id: int | str, payment: dict
    ) -> Response:
        """
        https://doc.gopay.com#partially-capturing-a-preauthorized-payment
        """
        return self.gopay.call(
            "POST",
            f"/payments/payment/{payment_id}/capture",
            ContentType.JSON,
            payment,
        )

    def void_authorization(self, payment_id: int | str) -> Response:
        """
        https://doc.gopay.com#voiding-a-preauthorized-payment
        """
        return self.gopay.call(
            "POST", f"/payments/payment/{payment_id}/void-authorization"
        )

    def get_card_details(self, card_id: int | str) -> Response:
        """
        https://doc.gopay.com#payment-card-inquiry
        """
        return self.gopay.call("GET", f"/payments/cards/{card_id}")

    def delete_card(self, card_id: int | str) -> Response:
        """
        https://doc.gopay.com#payment-card-deletion
        """
        return self.gopay.call("DELETE", f"/payments/cards/{card_id}")

    def get_payment_instruments(self, goid: int | str, currency: Currency) -> Response:
        """
        https://doc.gopay.com#available-payment-methods-for-a-currency
        """
        return self.gopay.call(
            "GET", f"/eshops/eshop/{goid}/payment-instruments/{currency}"
        )

    def get_payment_instruments_all(self, goid: int | str) -> Response:
        """
        https://doc.gopay.com#all-available-payment-methods
        """
        return self.gopay.call("GET", f"/eshops/eshop/{goid}/payment-instruments")

    def get_account_statement(self, statement_request: dict) -> Response:
        """
        https://doc.gopay.com#account-statement
        """
        return self.gopay.call(
            "POST", "/accounts/account-statement", ContentType.JSON, statement_request
        )

    def refund_payment_eet(self, payment_id: int | str, payment_data: dict) -> Response:
        return self.gopay.call(
            "POST",
            f"/payments/payment/{payment_id}/refund",
            ContentType.JSON,
            payment_data,
        )

    def get_eet_receipt_by_payment_id(self, payment_id: int | str) -> Response:
        return self.gopay.call("GET", f"/payments/payment/{payment_id}/eet-receipts")

    def find_eet_receipts_by_filter(self, filter: dict) -> Response:
        return self.gopay.call("POST", "/eet-receipts", ContentType.JSON, filter)

    @property
    def get_embedjs_url(self) -> str:
        return self.gopay.base_url[:-4] + "/gp-gw/js/embed.js"
