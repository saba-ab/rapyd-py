[![PyPI version](https://img.shields.io/pypi/v/rapyd-py.svg)](https://pypi.org/project/rapyd-py/)
[![Python versions](https://img.shields.io/pypi/pyversions/rapyd-py.svg)](https://pypi.org/project/rapyd-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/saba-ab/rapyd-py/actions/workflows/ci.yml/badge.svg)](https://github.com/saba-ab/rapyd-py/actions/workflows/ci.yml)

# rapyd-py

**The unofficial async Python SDK for Rapyd — the one Rapyd should have built.**

Fully async, Pydantic v2 models, webhook verification, auto-pagination, and complete coverage of all 6 Rapyd domains. Built to be the foundation for [rapyd-mcp](https://github.com/saba-ab/rapyd-mcp).

## Why This Exists

The official `rapyd-sdk` on PyPI is a bare-bones beta — no async support, no Pydantic models, no webhook signature verification, and incomplete endpoint coverage. This library fixes all of that.

## Install

```bash
pip install rapyd-py
```

## Quick Start

```python
import asyncio
from rapyd import RapydClient

async def main():
    async with RapydClient() as rapyd:
        # Create a payment
        payment = await rapyd.payments().create(
            amount=100.00,
            currency="USD",
            payment_method={
                "type": "us_visa_card",
                "fields": {
                    "number": "4111111111111111",
                    "expiration_month": "12",
                    "expiration_year": "29",
                    "cvv": "345",
                    "name": "John Doe",
                }
            },
            capture=True,
        )
        print(f"Payment created: {payment.id} — status: {payment.status}")

asyncio.run(main())
```

## Configuration

### Environment Variables (recommended)

```bash
export RAPYD_ACCESS_KEY=your_access_key
export RAPYD_SECRET_KEY=your_secret_key
export RAPYD_ENVIRONMENT=sandbox   # or "production"
```

Or use a `.env` file — the SDK reads it automatically.

### Explicit Arguments

```python
client = RapydClient(
    access_key="your_access_key",
    secret_key="your_secret_key",
    environment="sandbox",
    timeout=30,
)
```

## Domains

### Collect (Payments)

```python
# Payments
payment = await rapyd.payments().create(amount=50, currency="USD", ...)
payment = await rapyd.payments().get("payment_xxx")
payments = await rapyd.payments().list(limit=20)

# Refunds
refund = await rapyd.refunds().create(payment="payment_xxx", amount=10)

# Customers
customer = await rapyd.customers().create(name="Jane Doe", email="jane@example.com")

# Checkout
checkout = await rapyd.checkout().create(amount=100, country="US", currency="USD")

# Subscriptions & Plans
plan = await rapyd.plans().create(amount=29.99, currency="USD", interval="month", product="product_xxx")
sub = await rapyd.subscriptions().create(customer="cus_xxx", billing="pay_automatically", ...)
```

### Disburse (Payouts)

```python
payout = await rapyd.payouts().create(
    beneficiary="beneficiary_xxx",
    sender="sender_xxx",
    payout_amount=10000,
    payout_currency="PHP",
    payout_method_type="ph_metrobank_bank",
    ewallet="ewallet_xxx",
)
confirmed = await rapyd.payouts().confirm("payout_xxx")
```

### Wallet

```python
wallet = await rapyd.wallets().create(first_name="John", last_name="Doe", ...)
transfer = await rapyd.wallet_transfers().create(
    source_ewallet="ewallet_src",
    destination_ewallet="ewallet_dst",
    amount=500,
    currency="USD",
)
```

### Issuing (Cards)

```python
card = await rapyd.cards().create(ewallet_contact="cont_xxx", card_program="cardprog_xxx")
await rapyd.cards().activate(card=card.id)
await rapyd.cards().set_pin(card=card.id, pin="1234")
```

### Verify (KYC)

```python
identity = await rapyd.identities().create(country="US", document_type="passport", ...)
hosted = await rapyd.verification().create_hosted_page(country="US", ...)
```

### Protect (Fraud)

```python
settings = await rapyd.fraud().get_settings()
await rapyd.fraud().update_settings(enabled=True)
```

## Webhook Verification

```python
from fastapi import FastAPI, Request, Header
from rapyd import parse_webhook_event

app = FastAPI()

@app.post("/webhook")
async def webhook(
    request: Request,
    salt: str = Header(...),
    timestamp: str = Header(...),
    signature: str = Header(...),
):
    body = await request.body()
    event = parse_webhook_event(
        body,
        salt=salt,
        timestamp=timestamp,
        signature=signature,
        access_key="your_access_key",
        secret_key="your_secret_key",
        webhook_url="https://yourdomain.com/webhook",
    )
    print(f"Received {event.type}: {event.data}")
    return {"status": "ok"}
```

## Async Pagination

```python
from rapyd import paginate

async for payment in paginate(rapyd.payments().list, limit=50):
    print(payment.id)
```

## Error Handling

```python
from rapyd import RapydClient, RapydApiError, RapydAuthError

async with RapydClient() as rapyd:
    try:
        payment = await rapyd.payments().get("payment_nonexistent")
    except RapydAuthError as e:
        print(f"Auth failed: {e.error_code}")
    except RapydApiError as e:
        print(f"API error: {e.error_code} — {e.message}")
        print(f"Operation ID: {e.operation_id}")
```

## MCP Server

This SDK is the foundation for **rapyd-mcp** — a Model Context Protocol server for Rapyd. Coming soon.

## Contributing

1. Clone the repo
2. `pip install -e ".[dev]"`
3. `pytest` to run tests
4. `ruff check .` for linting

## Links

- [Official Rapyd Docs](https://docs.rapyd.net)
- [Rapyd API Reference](https://docs.rapyd.net/en/merchant-api-reference.html)
- [rapyd-mcp](https://github.com/saba-ab/rapyd-mcp) (coming soon)

## License

MIT
