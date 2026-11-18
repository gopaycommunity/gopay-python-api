# CLAUDE.md

## Project

GoPay's Python SDK (`gopay` on PyPI) — a thin wrapper over the GoPay Payments REST API (https://doc.gopay.com). Managed with Poetry (>= 2.0; metadata lives in the standard `[project]` table, Poetry-specific settings in `[tool.poetry]`); supports Python 3.9–3.15 (`requires-python = ">=3.9,<4.0"` in `pyproject.toml`, CI matrix 3.9–3.15; keep the matrix and the `Programming Language :: Python :: 3.x` classifiers in sync).

## Commands

```bash
poetry install                       # install deps incl. dev group
poetry run pytest tests/             # run all tests (adds --cov=gopay automatically)
poetry run pytest tests/test_api_payment.py::TestPayments::test_create_payment   # single test
poetry run ruff check .                                                           # lint (E, F, I, UP; config in pyproject.toml)
poetry run ruff check . --fix                                                     # apply safe lint fixes (incl. import sorting)
poetry run ruff format --check .                                                  # check formatting (CI)
poetry run ruff format .                                                          # format code
poetry run pyright                                                                # type check (config in pyproject.toml; gopay/ is strict)
poetry run pre-commit install                                                     # once: install git hook (ruff check/format, pyright, basic file checks)
poetry run pre-commit run --all-files                                             # run all hooks over the repo
```

Pre-commit hooks for Ruff and Pyright are `repo: local` and run via `poetry run`, so tool versions come from `poetry.lock` — don't switch them to the upstream mirror repos (that would pin versions twice). Tests are intentionally not a hook (they hit the network).

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

- Version lives in two places: `pyproject.toml` (`[project].version`) and `gopay/utils.py` (`VERSION`, used in the default User-Agent). Bump both together.
- `DEFAULT_TIMEOUT` (3600 s) is defined in `gopay/models.py` and reused by `api.py`/`http.py`.
- `Response.has_succeed()` is deprecated in favor of the `success` property; `Payments.get_embedjs_url` is a property, not a method.
- When adding an API method, also update the "Available methods" table in `README.md`.
- Ruff infers its target version from `requires-python`, so don't set `target-version` in `[tool.ruff]`; Pyright's `pythonVersion` is set explicitly and must track the lower bound. `keep-runtime-typing = true` is deliberate: Pydantic evaluates annotations at runtime, so `Optional[X]` must not become `X | None` while 3.9 is supported.
- `pyproject.toml` keeps the `License :: OSI Approved :: MIT License` classifier next to `license = "MIT"` on purpose (for tools that read only classifiers); Poetry warns it's deprecated — that warning is expected.
- `# fmt: off` / `# fmt: on` blocks in `gopay/api.py` and `gopay/services.py` keep `# pyright: ignore` comments on the line Pyright reports; don't remove them.
