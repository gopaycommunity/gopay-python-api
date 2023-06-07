from typing import Any
import requests
import logging
from dataclasses import dataclass, field


@dataclass
class Request:
    method: str = "get"
    url: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    body: dict = field(default_factory=dict)


@dataclass
class Response:
    raw_body: bytes
    json: dict
    status_code: int

    def has_succeed(self) -> bool:
        return self.status_code < 400

    def __str__(self) -> str:
        return self.raw_body.decode("utf-8")


class Browser:
    def __init__(self, logger: Any, timeout: int) -> None:
        self.logger = logger
        self.timeout = timeout

    def browse(self, request: Request):
        logging.debug(vars(request))
        try:
            r = requests.request(
                request.method,
                request.url,
                headers=request.headers,
                data=request.body,
                timeout=self.timeout,
            )
            response = Response(r.content, r.json(), r.status_code)
        except ValueError as ve:
            response = Response(r.content, None, r.status_code)
        except Exception as e:
            response = Response(e, {}, 500)
        self.logger(request, response)
        return response


def default_logger(request, response):
    logging.info(f"Request: {request}")
    logging.info(f"Response: {response}")
