# Changelog

## Unreleased

- Added Pyright static type checking, `gopay` checked in strict mode, tests and examples in standard mode, run in CI
- Added type annotations to the SDK (`JSONDict` alias for request and response bodies), public signatures are unchanged
- Package ships type information (`py.typed`, PEP 561)
- Fixed type of `AbstractCache.get_token()` to `AccessToken | None` and of `scope` in `ApiClient` and `AccessToken` to `TokenScope | str` to match actual values (no runtime change)
- Replaced Black, isort and flake8 with Ruff (lint and formatting), checked in CI
- Applied Ruff formatting to SDK sources, tests and examples (formatting only), the commit is listed in `.git-blame-ignore-revs`
- Added pre-commit hooks (Ruff, Pyright and basic file checks)
- CI tests also on Python 3.13, 3.14 and 3.15, `actions/checkout` and `actions/setup-python` bumped to v7
- CI tests also on Windows with Python 3.9
- CI runs Python 3.9 on Ubuntu 24.04, `ubuntu-latest` (26.04) has no Python 3.9 build, Python 3.9 jobs use Poetry 2.2.1 (Poetry 2.3+ requires Python 3.10)
- Added Dependabot for GitHub Actions and pip dependencies
- CI workflow restricted to read-only repository permissions (`permissions: contents: read`)
- `pyproject.toml` migrated to the standard `[project]` table (PEP 621), Poetry 2.0 or newer is required for development; package contents and metadata unchanged except `License-Expression: MIT` instead of `License: MIT`
- Added Python version classifiers 3.9–3.15
- Added CLAUDE.md
- Updated sandbox test data (account statement date range, on-demand recurrence payment ID)
- README: minimum Python version fixed to 3.9, Pydantic mentioned as a required dependency, added local development instructions

## 2.3.1

- Added QR payment feature (`Payments.get_qr_payment()`, `QrCodeFormat` enum)
- Request timeout defaults to 3600 seconds and must be a positive integer
- Network errors no longer raise, `Response` with `status_code` 0 is returned instead
- Missing `access_token` in the OAuth response no longer raises
- Bumped `requests` from 2.32.3 to 2.32.4

## 2.2.6

- Added bank swifts `REVOLUT_LT`, `BANK365_SK`

## 2.2.5

- Added bank swift `PARTNERS_BANK` (`PTBNCZPP`)

## 2.2.4

- Added QR payment swift (`QR_PAYMENT`)

## 2.2.3

- Fixed SDK version lookup failing in the installed package (missing `pyproject.toml`)

## 2.2.2

- Added default `User-Agent` with SDK version
- Added `custom_user_agent` config option

## 2.2.1

- Migrated to Pydantic V2 (`pydantic` ^2.8.2)
- Dropped Python 3.8
- Updated dev dependencies and CI workflows

## 2.2.0

- Added history of refunds
- Added BNPL payment method
- Added `BnplType` enum

## 2.1.0

- Added configurable request timeout (#22)
- Fixed codes of `Language.ESTONIAN` and `Language.SLOVENIAN`
- CI tests also on Python 3.12
- Bumped `requests`, `urllib3`, `certifi`, `idna` and `black`

## 2.0.1

- Fixed URL of the embed JS for the inline gateway (#16)
- Added Card ID tests

## 2.0.0

Major refactor of the SDK. Basic usage stays the same, but there are backward incompatible changes:

- Removed the `isProductionMode` config option, use `gateway_url` instead
- Removed the `timeout` config option
- Renamed many parameters (e.g. `payments.get_status(id_payment=1234)` is now `payments.get_status(payment_id=1234)`), positional parameters keep working
- Snake case is preferred in the config, camelCase still works
- Config is validated with Pydantic, undocumented options raise an error
- `Response.has_succeed()` deprecated in favor of the `Response.success` property
- Default services moved to `gopay.services` as `DefaultCache` and `default_logger`
- Removed methods no longer available in GoPay (e.g. SuperCASH)
- Added Card ID methods
- Project moved to `pyproject.toml` and Poetry, tests migrated to pytest

## v1.2.0

- Added SuperCASH batch features

## v1.0.0

- Call every API method without validation
- Cache access token
- Log HTTP communication
