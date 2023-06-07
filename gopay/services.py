from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Any, TYPE_CHECKING
import logging
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from gopay.http import Request, Response, AccessToken

LoggerType = Callable[["Request", "Response"], Any]


class AbstractCache(ABC):
    @abstractmethod
    def get_token(self, key: str) -> AccessToken:
        ...

    @abstractmethod
    def set_token(self, key: str, token: AccessToken) -> None:
        ...


def default_logger(request: Request, response: Response):
    logging.info(f"GoPay HTTP Request: {request}")
    logging.info(f"GoPay HTTP Response: {response}")


@dataclass
class DefaultCache(AbstractCache):
    tokens: dict[str, AccessToken] = field(default_factory=dict, init=False)

    def get_token(self, key: str) -> AccessToken | None:
        return self.tokens.get(key)

    def set_token(self, key: str, token: AccessToken) -> None:
        self.tokens[key] = token
