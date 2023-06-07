from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from gopay.http import AccessToken, Request, Response

LoggerType = Callable[["Request", "Response"], Any]


class AbstractCache(ABC):
    @abstractmethod
    def get_token(self, key: str) -> AccessToken:
        ...

    @abstractmethod
    def set_token(self, key: str, token: AccessToken) -> None:
        ...


def default_logger(request: Request, response: Response):
    logging.debug(f"GoPay HTTP Request: {request}")
    logging.debug(f"GoPay HTTP Response: {response}")


@dataclass
class DefaultCache(AbstractCache):
    tokens: dict[str, AccessToken] = field(default_factory=dict, init=False)

    def get_token(self, key: str) -> AccessToken | None:
        return self.tokens.get(key)

    def set_token(self, key: str, token: AccessToken) -> None:
        self.tokens[key] = token
