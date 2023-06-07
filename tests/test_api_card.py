from gopay import Payments
import logging


class TestCards:
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
