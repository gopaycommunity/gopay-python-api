from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from gopay.http import AccessToken, Request, Response

LoggerType = Callable[["Request", "Response"], Any]


class AbstractCache(ABC):
    """
    Abstract class for implementing custom caches used to cache the token
    """

    @abstractmethod
    def get_token(self, key: str) -> AccessToken:
        """
        Fetch a token with the specified key from the cache
        """
        ...

    @abstractmethod
    def set_token(self, key: str, token: AccessToken) -> None:
        """
        Save the token to the cache under the specified key
        """
        ...


def default_logger(request: Request, response: Response):
    """
    Logs the HTTP Request and Response when communicating with GoPay using logging.debug
    """
    logging.debug(f"GoPay HTTP Request: {request}")
    logging.debug(f"GoPay HTTP Response: {response}")


@dataclass
class DefaultCache(AbstractCache):
    """
    Default cache implementation just keeps the tokens in memory, it's only uselful
    as long as the object instance is alive
    """

    tokens: dict[str, AccessToken] = field(default_factory=dict, init=False)

    def get_token(self, key: str) -> AccessToken | None:
        """
        Fetch token from memory
        """
        return self.tokens.get(key)

    def set_token(self, key: str, token: AccessToken) -> None:
        """
        Save token to memory
        """
        self.tokens[key] = token
