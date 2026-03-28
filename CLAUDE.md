CLAUDE.md
markdown# CLAUDE.md — Rapyd Python SDK

## Project Purpose
Async Python SDK for the Rapyd Fintech-as-a-Service API.
Published to PyPI as `rapyd-py`. After completion, this SDK will be the
foundation for a Rapyd MCP server (rapyd-mcp). Build quality must match
a production open-source library — not a script.

## Source of Truth
`RAPYD_API_REFERENCE.md` in the project root is the single source of truth
for all endpoints, signing logic, webhook types, enums, and error codes.
Always read it before implementing any domain. Do not invent endpoints.

## Tech Stack
- Python 3.11+
- httpx (async HTTP client, NOT aiohttp, NOT requests)
- Pydantic v2 (models and settings)
- pydantic-settings (config from env)
- pytest + pytest-asyncio + pytest-httpx (testing)
- hatchling (build backend)

## Architecture — Mirror the Laravel SDK Pattern
The Laravel SDK pattern: one `RapydClient` class exposes resource accessors
(e.g. `payments()`, `wallets()`). Each resource is a class that holds a
reference to the client and implements its API methods.

Python equivalent:
```
rapyd/
  __init__.py          # public exports
  client.py            # RapydClient — main entry point
  auth.py              # HMAC-SHA256 request signing
  exceptions.py        # Exception hierarchy
  pagination.py        # Async generator for list endpoints
  webhooks.py          # Webhook signature verification + event parsing
  enums.py             # All Rapyd enums as Python StrEnum
  models/
    __init__.py
    base.py            # RapydModel, RapydResponse[T], RapydObject
    payment.py         # Payment, Refund, Customer, Checkout, Subscription...
    payout.py          # Payout, Beneficiary, Sender
    wallet.py          # Wallet, WalletContact, WalletTransaction, VirtualAccount
    issuing.py         # Card, CardProgram, CardTransaction
    verify.py          # Identity, VerificationApplication
    webhook.py         # WebhookEvent[T]
  resources/
    __init__.py
    base.py            # BaseResource (holds client ref, helper methods)
    payments.py        # PaymentsResource
    refunds.py         # RefundsResource
    customers.py       # CustomersResource
    checkout.py        # CheckoutResource
    payment_links.py   # PaymentLinksResource
    payment_methods.py # PaymentMethodsResource
    subscriptions.py   # SubscriptionsResource
    plans.py           # PlansResource
    products.py        # ProductsResource
    invoices.py        # InvoicesResource
    disputes.py        # DisputesResource
    payouts.py         # PayoutsResource
    beneficiaries.py   # BeneficiariesResource
    senders.py         # SendersResource
    payout_methods.py  # PayoutMethodsResource
    wallets.py         # WalletsResource
    wallet_contacts.py # WalletContactsResource
    wallet_transfers.py# WalletTransfersResource
    wallet_transactions.py
    virtual_accounts.py
    cards.py           # CardsResource
    card_programs.py   # CardProgramsResource
    identities.py      # IdentitiesResource
    verification.py    # VerificationResource
    fraud.py           # FraudResource
    data.py            # DataResource (countries, currencies, FX)
```

## Signing — CRITICAL
Read Section 2.2 of RAPYD_API_REFERENCE.md before touching auth.py.

Pipeline: HMAC-SHA256 → hex string → base64 of the hex string.
The most common Python bug: base64-encoding the raw digest bytes instead
of the hex string. Rapyd will silently reject every request.
```python
# CORRECT
raw = hmac.new(secret.encode(), to_sign.encode(), sha256).digest()
sig  = base64.b64encode(raw.hex().encode()).decode()

# WRONG — Rapyd rejects this
sig  = base64.b64encode(raw).decode()
```

Body serialisation: `json.dumps(body, separators=(",", ":"))` — no spaces.
GET / empty body = `""` not `"{}"`.

## Response Handling
Every response is unwrapped from the envelope:
```json
{ "status": { "status": "SUCCESS" }, "data": { ... } }
```
If `status.status != "SUCCESS"`, raise `RapydApiError`.
The resource methods return the typed `data` object, never the raw envelope.

## Async First
All HTTP methods on `RapydClient` are `async def`.
`RapydClient` is an async context manager:
```python
async with RapydClient() as rapyd:
    payment = await rapyd.payments().get("payment_xxx")
```
Also support explicit `await rapyd.aclose()`.

## MCP Readiness — Design Constraint
Every resource method must have a detailed docstring because the MCP server
will use these docstrings as tool descriptions. No docstring = broken MCP tool.

Format:
```python
async def create(self, **kwargs) -> Payment:
    """
    Create a payment.

    Args:
        amount: Payment amount as a positive float.
        currency: ISO 4217 currency code (e.g. "USD", "GEL").
        payment_method: Payment method type string.
        country: ISO 3166-1 alpha-2 country code.
        ...
    Returns:
        Payment object with id, status, redirect_url, etc.
    Rapyd docs: https://docs.rapyd.net
    """
```

## Config / Environment
```python
from pydantic_settings import BaseSettings

class RapydSettings(BaseSettings):
    rapyd_access_key: str
    rapyd_secret_key: str
    rapyd_environment: str = "sandbox"  # "sandbox" | "production"
    rapyd_timeout: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
```

## Error Hierarchy
```
RapydException
  RapydApiError       — API returned status=ERROR
    RapydAuthError    — UNAUTHORIZED_API_CALL / UNAUTHENTICATED
  RapydValidationError
  RapydWebhookError
  RapydTimeoutError
  RapydConnectionError
```

## Pagination
List methods accept `limit`, `page`, `starting_after`, `ending_before`.
`pagination.py` provides an async generator `paginate()` that auto-fetches
next pages. Resource list methods call this internally.

## Testing
- pytest-httpx to mock httpx requests
- One test file per domain
- Test signing logic independently in `test_auth.py`
- Never make real HTTP calls in tests

## PyPI Publishing
Package name: `rapyd-py`
```
pip install rapyd-py
```
```python
from rapyd import RapydClient
```
```

---

## Phase Prompts

---

### Phase 1 — Project Scaffold
```
Read RAPYD_API_REFERENCE.md and CLAUDE.md.

Set up the complete Python SDK project scaffold:

1. `pyproject.toml` using hatchling build backend.
   - Package name: rapyd-py
   - Version: 1.0.0
   - Python >=3.11
   - Dependencies: httpx>=0.27, pydantic>=2.7, pydantic-settings>=2.3
   - Dev deps: pytest, pytest-asyncio, pytest-httpx, ruff, mypy, python-dotenv
   - pytest asyncio_mode = "auto"

2. `.env.example`:
   RAPYD_ACCESS_KEY=your_access_key_here
   RAPYD_SECRET_KEY=your_secret_key_here
   RAPYD_ENVIRONMENT=sandbox

3. `.gitignore` — Python standard (venv, __pycache__, .env, dist, *.egg-info)

4. All empty `__init__.py` files for:
   rapyd/
   rapyd/models/
   rapyd/resources/

5. `README.md` — minimal skeleton with install instructions and a usage
   teaser showing: `async with RapydClient() as rapyd: payment = await rapyd.payments().get("payment_xxx")`

Do not write any logic yet. Scaffold only.
```

---

### Phase 2 — Config & Exceptions
```
Read RAPYD_API_REFERENCE.md sections 9 (Error Handling) and CLAUDE.md.

Implement two files:

--- rapyd/config.py ---
RapydSettings using pydantic-settings BaseSettings:
- rapyd_access_key: str
- rapyd_secret_key: str
- rapyd_environment: Literal["sandbox", "production"] = "sandbox"
- rapyd_timeout: int = 30
- base_url property that returns sandboxapi.rapyd.net or api.rapyd.net

--- rapyd/exceptions.py ---
Full exception hierarchy as defined in CLAUDE.md:
  RapydException (base)
  RapydApiError(RapydException)
    - fields: error_code, status_code, operation_id, message, raw: dict
    - __repr__ includes all fields
  RapydAuthError(RapydApiError)
  RapydValidationError(RapydException)
    - fields: message, field
  RapydWebhookError(RapydException)
  RapydTimeoutError(RapydException)
  RapydConnectionError(RapydException)

All classes must have docstrings.
```

---

### Phase 3 — Auth & Request Signing
```
Read RAPYD_API_REFERENCE.md section 2.2 (Authentication) and 2.4 (Webhook Signing) carefully.
Read CLAUDE.md section "Signing — CRITICAL".

Implement rapyd/auth.py with these functions:

1. _random_salt(length=12) -> str
   Random alphanumeric string, 8-16 chars.

2. _unix_timestamp() -> str
   Current Unix time as string.

3. _compact_json(body: dict | None) -> str
   json.dumps with separators=(",",":"). Empty string for None/empty dict.

4. sign_request(*, http_method, url_path, access_key, secret_key, body=None, salt=None, timestamp=None) -> dict[str, str]
   Returns dict with keys: access_key, salt, timestamp, signature.
   Signing pipeline:
     to_sign = method.lower() + path + salt + ts + access_key + secret_key + body_string
     raw     = hmac.new(secret_key.encode(), to_sign.encode(), sha256).digest()
     sig     = base64.b64encode(raw.hex().encode()).decode()

5. verify_webhook_signature(*, url_path, salt, timestamp, signature, access_key, secret_key, body_string) -> bool
   Webhook formula: NO http_method prefix.
   to_sign = url_path + salt + ts + access_key + secret_key + body_string
   Same hex→base64 pipeline. Use hmac.compare_digest for timing-safe comparison.

Write tests in tests/test_auth.py:
- test that signing a known input produces the expected signature
- test that wrong secret_key fails verify_webhook_signature
- test _compact_json("") returns "" not "{}"
- test sign_request with GET (no body) produces empty body_string
```

---

### Phase 4 — Async HTTP Client
```
Read RAPYD_API_REFERENCE.md sections 2.1, 2.2, 2.3, 2.5, 9.
Read CLAUDE.md "Async First" and "Response Handling" sections.

Implement rapyd/http.py — the internal async HTTP layer that all resources use.

Class: RapydHttpClient

Constructor: __init__(self, settings: RapydSettings)
  - Creates an httpx.AsyncClient with:
    - base_url from settings
    - timeout from settings
    - default headers: Content-Type: application/json

Methods (all async):

async def request(self, method: str, path: str, *, body: dict | None = None, params: dict | None = None, idempotency_key: str | None = None) -> dict
  - Calls sign_request() to get auth headers
  - Adds optional idempotency header (auto-generates one for POST if not provided: f"{timestamp}-{salt}")
  - Builds query string from params, appends to path for signing
  - Makes the httpx request
  - Parses JSON response
  - Calls _handle_response() to check for errors
  - Returns the raw dict

async def get(self, path: str, *, params: dict | None = None) -> dict
async def post(self, path: str, *, body: dict | None = None, idempotency_key: str | None = None) -> dict
async def put(self, path: str, *, body: dict | None = None) -> dict
async def delete(self, path: str) -> dict

_handle_response(self, data: dict, status_code: int) -> dict
  - If data["status"]["status"] != "SUCCESS": raise appropriate exception
  - HTTP 401/403 → RapydAuthError
  - Other errors → RapydApiError with error_code, operation_id, message
  - Returns data on success

async def aclose(self) -> None
  - Closes the underlying httpx.AsyncClient

Implement as async context manager (__aenter__ / __aexit__).

Write tests in tests/test_http.py using pytest-httpx to mock responses.
Test: successful GET, successful POST, error response raises RapydApiError,
401 raises RapydAuthError, httpx timeout raises RapydTimeoutError.
```

---

### Phase 5 — Pydantic Models
```
Read RAPYD_API_REFERENCE.md sections 3, 5, 11.
Read CLAUDE.md "Tech Stack" and architecture section.

Implement all model files. Use Pydantic v2. All models extend RapydModel.
Use model_config = ConfigDict(extra="allow", populate_by_name=True)
so new Rapyd API fields never break existing code.

--- rapyd/models/base.py ---
- RapydModel(BaseModel): base config
- RapydStatus: error_code, status, message, response_code, operation_id. Property: is_success, is_error
- RapydResponse[T](Generic[T]): status: RapydStatus, data: T | None, has_more: bool, total_count: int | None
- RapydObject(RapydModel): id: str = ""
- RapydAddress: name, line_1, line_2, city, state, country, zip, phone_number

--- rapyd/models/payment.py ---
Models: Payment, Refund, Customer, Checkout, PaymentLink, Plan, Subscription,
Product, Invoice, Dispute. All fields from section 3.1.

--- rapyd/models/payout.py ---
Models: Payout, Beneficiary, Sender. Fields from section 3.2.

--- rapyd/models/wallet.py ---
Models: Wallet, WalletAccount, WalletContact, WalletTransaction, WalletTransfer,
VirtualAccount. Fields from section 3.3.

--- rapyd/models/issuing.py ---
Models: Card, CardProgram, CardTransaction. Fields from section 3.4.

--- rapyd/models/verify.py ---
Models: Identity, VerificationApplication. Fields from section 3.5.

--- rapyd/models/webhook.py ---
WebhookEvent[T](Generic[T]):
  id: str
  type: str         # e.g. "PAYMENT_COMPLETED"
  data: T | None    # typed payload
  trigger_operation_id: str
  status: str
  created_at: int

--- rapyd/enums.py ---
All enums from section 5 as Python StrEnum (not PHP backed enums).
PaymentStatus, PaymentMethodCategory, PaymentFlowType, NextAction,
RefundStatus, DisputeStatus, PayoutStatus, PayoutMethodCategory,
SubscriptionStatus, InvoiceStatus, WebhookStatus, CardStatus,
CardBlockReasonCode, WalletStatus, WalletContactType, IdentityStatus.

--- rapyd/models/__init__.py ---
Export all models.
```

---

### Phase 6 — Base Resource
```
Read CLAUDE.md "MCP Readiness" section.
Read RAPYD_API_REFERENCE.md section 8 (Pagination).

Implement rapyd/resources/base.py:

Class: BaseResource
  __init__(self, client: RapydHttpClient)  — stores the client

Protected helpers:
  async def _get(self, path: str, *, params: dict | None = None) -> dict
  async def _post(self, path: str, *, body: dict | None = None, idempotency_key: str | None = None) -> dict
  async def _put(self, path: str, *, body: dict | None = None) -> dict
  async def _delete(self, path: str) -> dict

  def _build_list_params(self, limit: int | None, page: int | None, starting_after: str | None, ending_before: str | None) -> dict
    Builds the pagination query params dict, only including non-None values.

  def _extract_data(self, response: dict) -> dict | list
    Returns response["data"] — convenience helper.

Implement rapyd/pagination.py:

async def paginate(resource_method, **kwargs) -> AsyncGenerator[Any, None]:
  """
  Async generator that auto-paginates a list endpoint.

  Usage:
      async for payment in paginate(rapyd.payments().list, limit=50):
          print(payment.id)

  Fetches pages sequentially using starting_after cursor until no more results.
  """
```

---

### Phase 7 — Collect Resources (Payments Domain)
```
Read RAPYD_API_REFERENCE.md section 3.1 carefully. Every endpoint listed
there must be implemented. Read CLAUDE.md "MCP Readiness" — every method
needs a proper docstring.

Implement these resource files in rapyd/resources/:

payments.py — PaymentsResource
  create(**kwargs) -> Payment
  get(payment_id: str) -> Payment
  update(payment_id: str, **kwargs) -> Payment
  cancel(payment_id: str) -> Payment
  list(limit, page, starting_after, ending_before) -> list[Payment]
  capture(payment_id: str, **kwargs) -> Payment
  complete(payment_id: str, amount: float) -> Payment  # sandbox only

refunds.py — RefundsResource
  create(**kwargs) -> Refund
  get(refund_id: str) -> Refund
  update(refund_id: str, **kwargs) -> Refund
  list(...) -> list[Refund]
  list_by_payment(payment_id: str) -> list[Refund]

customers.py — CustomersResource
  create(**kwargs) -> Customer
  get(customer_id: str) -> Customer
  update(customer_id: str, **kwargs) -> Customer
  delete(customer_id: str) -> dict
  list(...) -> list[Customer]
  add_payment_method(customer_id: str, **kwargs) -> dict
  list_payment_methods(customer_id: str) -> list[dict]
  delete_payment_method(customer_id: str, pm_id: str) -> dict

checkout.py — CheckoutResource
  create(**kwargs) -> Checkout
  get(checkout_id: str) -> Checkout

payment_links.py — PaymentLinksResource
  create(**kwargs) -> PaymentLink
  get(link_id: str) -> PaymentLink
  list(...) -> list[PaymentLink]

payment_methods.py — PaymentMethodsResource
  list_by_country(country: str) -> list[dict]
  required_fields(payment_method_type: str) -> dict

subscriptions.py — SubscriptionsResource
  create(**kwargs) -> Subscription
  get(sub_id: str) -> Subscription
  update(sub_id: str, **kwargs) -> Subscription
  cancel(sub_id: str) -> Subscription
  list(...) -> list[Subscription]

plans.py — PlansResource
  create / get / update / delete / list

products.py — ProductsResource
  create / get / update / delete / list

invoices.py — InvoicesResource
  create / get / update / delete / list
  finalize(invoice_id: str) -> Invoice
  pay(invoice_id: str, **kwargs) -> Invoice

disputes.py — DisputesResource
  get(dispute_id: str) -> dict
  list(...) -> list[dict]
```

---

### Phase 8 — Disburse Resources (Payouts Domain)
```
Read RAPYD_API_REFERENCE.md section 3.2 carefully.

Implement in rapyd/resources/:

payouts.py — PayoutsResource
  create(**kwargs) -> Payout
  get(payout_id: str) -> Payout
  update(payout_id: str, **kwargs) -> Payout
  cancel(payout_id: str) -> Payout
  list(...) -> list[Payout]
  confirm(payout_id: str) -> Payout
  complete(payout_id: str, amount: float) -> Payout  # sandbox
  set_response(payout_id: str, **kwargs) -> Payout

beneficiaries.py — BeneficiariesResource
  create(**kwargs) -> Beneficiary
  get(beneficiary_id: str) -> Beneficiary
  update(beneficiary_id: str, **kwargs) -> Beneficiary
  delete(beneficiary_id: str) -> dict
  list(...) -> list[Beneficiary]

senders.py — SendersResource
  create / get / update / delete / list

payout_methods.py — PayoutMethodsResource
  list(country=None, currency=None, ...) -> list[dict]
  list_types(payout_id: str) -> list[dict]
  required_fields(payout_method_type: str) -> dict
```

---

### Phase 9 — Wallet Resources
```
Read RAPYD_API_REFERENCE.md section 3.3 carefully.

Implement in rapyd/resources/:

wallets.py — WalletsResource
  create(**kwargs) -> Wallet
  get(wallet_id: str) -> Wallet
  update(wallet_id: str, **kwargs) -> Wallet
  delete(wallet_id: str) -> dict
  list(...) -> list[Wallet]

wallet_contacts.py — WalletContactsResource
  create(wallet_id: str, **kwargs) -> WalletContact
  get(wallet_id: str, contact_id: str) -> WalletContact
  update(wallet_id: str, contact_id: str, **kwargs) -> WalletContact
  delete(wallet_id: str, contact_id: str) -> dict
  list(wallet_id: str, ...) -> list[WalletContact]

wallet_transfers.py — WalletTransfersResource
  create(**kwargs) -> WalletTransfer
  set_response(**kwargs) -> WalletTransfer

wallet_transactions.py — WalletTransactionsResource
  list(wallet_id: str, ...) -> list[WalletTransaction]
  get(wallet_id: str, transaction_id: str) -> WalletTransaction

virtual_accounts.py — VirtualAccountsResource
  create(**kwargs) -> VirtualAccount
  get(va_id: str) -> VirtualAccount
  update(va_id: str, **kwargs) -> VirtualAccount
  close(va_id: str) -> dict
  list(...) -> list[VirtualAccount]
```

---

### Phase 10 — Issuing, Verify, Protect, Data Resources
```
Read RAPYD_API_REFERENCE.md sections 3.4, 3.5, 3.6, 3.7.

Implement in rapyd/resources/:

cards.py — CardsResource
  create(**kwargs) -> Card
  get(card_id: str) -> Card
  update(card_id: str, **kwargs) -> Card
  update_status(**kwargs) -> Card
  activate(**kwargs) -> Card
  list(...) -> list[Card]
  list_transactions(card_id: str, ...) -> list[dict]
  set_pin(**kwargs) -> dict
  get_pin(**kwargs) -> dict

card_programs.py — CardProgramsResource
  create(**kwargs) -> CardProgram
  get(program_id: str) -> CardProgram
  list(...) -> list[CardProgram]

identities.py — IdentitiesResource
  create(**kwargs) -> Identity
  get(identity_id: str) -> Identity
  list(...) -> list[Identity]

verification.py — VerificationResource
  create_hosted_page(**kwargs) -> dict
  get_application_status(application_id: str) -> dict

fraud.py — FraudResource
  get_settings() -> dict
  update_settings(**kwargs) -> dict

data.py — DataResource
  countries() -> list[dict]
  currencies() -> list[dict]
  fx_rate(**kwargs) -> dict
  daily_rate(**kwargs) -> dict
```

---

### Phase 11 — Webhook Handler
```
Read RAPYD_API_REFERENCE.md sections 2.4 and 4 (all webhook event types).

Implement rapyd/webhooks.py:

Function: parse_webhook_event(payload: str | bytes, *, salt: str, timestamp: str, signature: str, access_key: str, secret_key: str, webhook_url: str) -> WebhookEvent

Steps:
1. Call verify_webhook_signature() from auth.py. Raise RapydWebhookError if invalid.
2. Parse the payload JSON.
3. Map the "type" field to the correct data model using a WEBHOOK_TYPE_MAP dict.
   Example entries:
     "PAYMENT_COMPLETED"   -> Payment
     "PAYOUT_COMPLETED"    -> Payout
     "WALLET_TRANSACTION"  -> WalletTransaction
     "CARD_ISSUING_SALE"   -> dict (raw for untyped events)
   All 40+ webhook types from section 4 must be in the map.
4. Deserialise event["data"]["body"] (or event["data"]) into the mapped model.
5. Return WebhookEvent[T] with all fields populated.

Also implement a WebhookHandler class for frameworks that prefer OOP:
  on(event_type: str, handler: Callable) -> None  (registers a handler)
  dispatch(event: WebhookEvent) -> None            (calls registered handler)

Write tests/test_webhooks.py:
- Test valid signature passes
- Test tampered body raises RapydWebhookError
- Test PAYMENT_COMPLETED event deserialises to Payment model
```

---

### Phase 12 — Main Client & Package Init
```
Read CLAUDE.md "Async First" and architecture sections.

Implement rapyd/client.py — RapydClient, the main entry point:

class RapydClient:
  def __init__(self, *, access_key: str | None = None, secret_key: str | None = None,
               environment: str = "sandbox", timeout: int = 30, settings: RapydSettings | None = None)
    - If settings not provided, build from args or fall back to env vars via RapydSettings()
    - Creates RapydHttpClient internally

  # Resource accessors — lazy-instantiated, cached as _payments etc.
  def payments(self) -> PaymentsResource
  def refunds(self) -> RefundsResource
  def customers(self) -> CustomersResource
  def checkout(self) -> CheckoutResource
  def payment_links(self) -> PaymentLinksResource
  def payment_methods(self) -> PaymentMethodsResource
  def subscriptions(self) -> SubscriptionsResource
  def plans(self) -> PlansResource
  def products(self) -> ProductsResource
  def invoices(self) -> InvoicesResource
  def disputes(self) -> DisputesResource
  def payouts(self) -> PayoutsResource
  def beneficiaries(self) -> BeneficiariesResource
  def senders(self) -> SendersResource
  def payout_methods(self) -> PayoutMethodsResource
  def wallets(self) -> WalletsResource
  def wallet_contacts(self) -> WalletContactsResource
  def wallet_transfers(self) -> WalletTransfersResource
  def wallet_transactions(self) -> WalletTransactionsResource
  def virtual_accounts(self) -> VirtualAccountsResource
  def cards(self) -> CardsResource
  def card_programs(self) -> CardProgramsResource
  def identities(self) -> IdentitiesResource
  def verification(self) -> VerificationResource
  def fraud(self) -> FraudResource
  def data(self) -> DataResource

  Async context manager: __aenter__ returns self, __aexit__ calls aclose()
  async def aclose(self) -> None

Implement rapyd/__init__.py — public API:
  from rapyd.client import RapydClient
  from rapyd.exceptions import (RapydException, RapydApiError, RapydAuthError,
    RapydValidationError, RapydWebhookError, RapydTimeoutError)
  from rapyd.webhooks import parse_webhook_event, WebhookHandler
  from rapyd.pagination import paginate
  from rapyd.enums import *

  __all__ = [...]
  __version__ = "1.0.0"
```

---

### Phase 13 — Tests
```
Read tests/ directory. Write full test coverage for remaining domains.
Use pytest-httpx to mock all HTTP calls. Never make real API calls.

tests/test_payments.py
  - test create_payment returns Payment model
  - test get_payment returns Payment model
  - test cancel_payment calls DELETE
  - test list_payments returns list[Payment]
  - test API error raises RapydApiError with correct error_code

tests/test_payouts.py
  - test create_payout returns Payout model
  - test confirm_payout calls correct path
  - test list_payouts returns list[Payout]

tests/test_wallets.py
  - test create_wallet returns Wallet model
  - test wallet_contact_create returns WalletContact
  - test wallet_transfer_create returns WalletTransfer

tests/test_pagination.py
  - test paginate() iterates across 3 pages and yields all items

tests/test_client.py
  - test RapydClient initialises from env vars
  - test RapydClient as async context manager calls aclose
  - test resource accessors return correct types and are cached
```

---

### Phase 14 — README & PyPI Setup
```
Write the production-quality README.md for the rapyd-py PyPI package.

Must include:
1. Badges: PyPI version, Python versions, License, GitHub Actions
2. One-line pitch: "The unofficial async Python SDK for Rapyd — the one Rapyd should have built."
3. Why this exists (official rapyd-py on PyPI is abandoned — no async, no Pydantic, no webhook verification)
4. Install: pip install rapyd-py
5. Quick start — complete working example showing payment creation
6. Config section (env vars and explicit args both)
7. All 6 domains with code examples (Collect, Disburse, Wallet, Issuing, Verify, Protect)
8. Webhook verification example with FastAPI snippet
9. Async pagination example
10. Error handling example with try/except RapydApiError
11. MCP Server section: "This SDK is the foundation for rapyd-mcp — coming soon"
12. Contributing section
13. Link to official Rapyd docs

Also add to pyproject.toml:
- GitHub Actions workflow: .github/workflows/publish.yml
  On push to tag v*: run tests, then publish to PyPI using PYPI_TOKEN secret
- .github/workflows/ci.yml
  On every push/PR: ruff lint, mypy, pytest