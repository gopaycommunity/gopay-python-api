from gopay.http import Request, Response, AccessToken
from gopay.enums import TokenScope
from datetime import datetime
from gopay.services import DefaultCache, default_logger


class TestServices:
    def test_logger(self, mock_request: Request, mock_response: Response):
        result = default_logger(mock_request, mock_response)
        assert result is None

    def test_cache(self):
        key = "test_key"
        token = AccessToken("test_token", datetime.now(), TokenScope.ALL)
        cache = DefaultCache()

        cache.set_token(key, token)

        loaded_token = cache.get_token(key)

        assert loaded_token is not None
        assert loaded_token.token == token.token
        assert loaded_token.last_updated == token.last_updated
        assert loaded_token.scope == token.scope
