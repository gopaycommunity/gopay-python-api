# CLAUDE.md

## Project

GoPay's Python SDK (`gopay` on PyPI) — a thin wrapper over the GoPay Payments REST API (https://doc.gopay.com). Managed with Poetry; supports Python 3.9–3.12 (`python = "^3.9"` in `pyproject.toml`, CI matrix 3.9–3.12).

## Commands

```bash
poetry install                       # install deps incl. dev group
poetry run pytest tests/             # run all tests (adds --cov=gopay automatically)
poetry run pytest tests/test_api_payment.py::TestPayments::test_create_payment   # single test
poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics    # CI's blocking lint
poetry run flake8 . --max-complexity=10 --max-line-length=127                    # CI's non-blocking lint
poetry run black . && poetry run isort .                                          # formatting (isort uses black profile)
```

### Tests hit the real GoPay sandbox

Almost all tests are integration tests: `pytest-dotenv` loads `tests/.sandbox.env` (`GOID`, `CLIENT_ID`, `CLIENT_SECRET`, `GATEWAY_URL`) and fixtures in `tests/conftest.py` build a real client. Constructing `ApiClient` (and therefore `GoPay` / `gopay.payments(...)`) immediately requests an OAuth token in `__post_init__`, so even "construction" tests need network access. Several tests assert against hardcoded sandbox payment IDs and their expected states/errors. Only `test_services.py` and parts of `test_http.py` are pure unit tests.

## Architecture

Request flow is layered across four modules:

1. **`gopay/__init__.py` → `payments(config, services)`** — the public entry point. Normalizes camelCase config keys (`clientId`, `gatewayUrl`, …) to snake_case, validates via the Pydantic model `GopayConfig` (`gopay/models.py`, `extra="forbid"`, so unknown config keys raise), then builds `GoPay` and wraps it in `Payments`.
2. **`gopay/payments.py` → `Payments`** — one method per API endpoint; just maps to `gopay.call(method, path, content_type, body, params)`. `create_payment` injects default `target` (from `goid`) and `lang`. New endpoints go here.
3. **`gopay/api.py` → `GoPay`** — normalizes `gateway_url` to `scheme://host/api`, builds the `ApiClient` from config + optional `services` (`logger`, `cache`), and sets default headers (Accept, User-Agent, Accept-Language derived from `language`).
4. **`gopay/http.py` → `ApiClient`** — handles OAuth2 client-credentials token (cached via `AbstractCache`, key = `client_id-gateway_url-scope`, treated as expired after 30 min), sends via `requests`, and returns a `Response` dataclass. Form vs. JSON body is chosen by `ContentType`.

Key behavioral contract: **the SDK never raises on API/network errors.** `send_request` catches `requests.RequestException` and returns `Response(status_code=0)`; callers check `response.success` (`status_code < 400`). Preserve this when changing HTTP code.

Pluggable services (`gopay/services.py`): `AbstractCache` (`get_token`/`set_token`, default in-memory `DefaultCache`) and a logger callable `(Request, Response) -> Any` (default logs via `logging.debug`).

`gopay/enums.py` holds the API enums (currencies, swift codes, payment instruments, token scopes, languages, `ContentType`, `QrCodeFormat`, …).

## Conventions / gotchas

- Version lives in two places: `pyproject.toml` and `gopay/utils.py` (`VERSION`, used in the default User-Agent). Bump both together.
- `DEFAULT_TIMEOUT` (3600 s) is defined in `gopay/models.py` and reused by `api.py`/`http.py`.
- `Response.has_succeed()` is deprecated in favor of the `success` property; `Payments.get_embedjs_url` is a property, not a method.
- When adding an API method, also update the "Available methods" table in `README.md`.
