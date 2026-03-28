# Rapyd API — Complete Reference & Implementation Guide

> **Purpose**: This document is the single source of truth for all Rapyd API integration work in this project.
> It covers authentication, every endpoint, webhooks, enums, implementation flows, and testing.
> This is language-agnostic — use it for building PHP/Laravel SDKs, Python SDKs, MCP servers, or any integration.
> 
> **Source**: Compiled from https://docs.rapyd.net (official documentation)
> **Last updated**: March 2026

---

## 1. Overview

Rapyd is a fintech-as-a-service platform operating in 100+ countries with 1,200+ payment methods.
The API is organized into 6 domains:

| Domain | What it does | API prefix |
|--------|-------------|------------|
| **Collect** | Accept payments (cards, bank transfers, e-wallets, cash) | `/v1/payments`, `/v1/checkout`, `/v1/customers` |
| **Disburse** | Send payouts to 190+ countries | `/v1/payouts`, `/v1/payouts/beneficiary` |
| **Wallet** | Hold, transfer, and manage funds | `/v1/user`, `/v1/account/transfer` |
| **Issuing** | Issue virtual and physical cards | `/v1/issuing/cards` |
| **Verify** | KYC/KYB identity verification | `/v1/identities`, `/v1/hosted/idv` |
| **Protect** | Fraud detection and prevention | `/v1/fraud/merchant/settings` |

---

## 2. Rapyd API Fundamentals

### 2.1 Base URLs

| Environment | Base URL |
|---|---|
| Sandbox | `https://sandboxapi.rapyd.net` |
| Production | `https://api.rapyd.net` |

All paths start with `/v1/`.

### 2.2 Authentication — Request Signing

Every request requires these headers:

| Header | Value |
|---|---|
| `Content-Type` | `application/json` |
| `access_key` | API access key from Rapyd Client Portal |
| `salt` | Random string, 8-16 chars, unique per request |
| `timestamp` | Unix time in seconds (must be within 60s of actual time) |
| `signature` | Calculated HMAC-SHA256 signature |
| `idempotency` | Optional. Unique string to prevent duplicate operations |

#### Signature Formula

```
signature = BASE64( HEX( HMAC-SHA256( http_method + url_path + salt + timestamp + access_key + secret_key + body_string ) ) )
```

**CRITICAL implementation detail**: The signing pipeline is HMAC-SHA256 digest → convert to **hex string** → Base64 encode that hex string. You CANNOT Base64 encode the raw binary digest directly — Rapyd will reject it.

#### Signing Rules
- `http_method` must be **lowercase**: `get`, `post`, `put`, `delete`
- `url_path` is everything after the base URL, starting with `/v1/`. Include query params with `?` if present
- `body_string` is JSON with **no whitespace** except inside string values. For GET or empty bodies, use empty string `""` — NOT `"{}"`
- `secret_key` is used as the HMAC key AND also concatenated into the signing string
- The HMAC key for `hash_hmac()` is the `secret_key`

#### PHP Signature Implementation (reference)

```php
$toSign = $httpMethod . $urlPath . $salt . $timestamp . $accessKey . $secretKey . $bodyString;
$hmac = hash_hmac('sha256', $toSign, $secretKey); // Returns hex string
$signature = base64_encode($hmac);
```

This is simple in PHP because `hash_hmac()` returns hex by default. The pitfall in other languages is manually converting binary→hex→base64.

### 2.3 Response Envelope

Every Rapyd response follows this structure:

```json
{
  "status": {
    "error_code": "",
    "status": "SUCCESS",
    "message": "",
    "response_code": "",
    "operation_id": "uuid-here"
  },
  "data": { ... }
}
```

On error: `status.status` = `"ERROR"`, `error_code` and `message` populated, `data` may be null/absent.

For list endpoints, `data` is an array. Some list endpoints return pagination info in the top-level response (not inside `data`).

### 2.4 Webhook Signature Verification

Webhook signature uses a **different formula** than request signatures:

```
signature = BASE64( HMAC-SHA256( url_path + salt + timestamp + access_key + secret_key + body_string ) )
```

Note: **No `http_method` prefix**. The `url_path` is the full webhook URL configured in the Rapyd Client Portal.

Webhook headers contain: `Content-Type`, `salt`, `timestamp`, `signature`.

### 2.5 Idempotency

Optional `idempotency` header (unique string per request). The SDK should auto-generate one for POST requests (timestamp + salt), but allow override.

---

## 3. Complete Endpoint Map

### 3.1 Collect (Payments)

| Method | Path | Description | Resource Method |
|---|---|---|---|
| POST | `/v1/payments` | Create payment | `payments()->create()` |
| GET | `/v1/payments/{id}` | Retrieve payment | `payments()->get()` |
| PUT | `/v1/payments/{id}` | Update payment | `payments()->update()` |
| DELETE | `/v1/payments/{id}` | Cancel payment | `payments()->cancel()` |
| GET | `/v1/payments` | List payments | `payments()->list()` / `payments()->all()` |
| POST | `/v1/payments/{id}/capture` | Capture payment | `payments()->capture()` |
| POST | `/v1/refunds` | Create refund | `refunds()->create()` |
| GET | `/v1/refunds/{id}` | Retrieve refund | `refunds()->get()` |
| PUT | `/v1/refunds/{id}` | Update refund | `refunds()->update()` |
| GET | `/v1/refunds` | List refunds | `refunds()->list()` |
| GET | `/v1/payments/{id}/refunds` | List refunds by payment | `refunds()->listByPayment()` |
| POST | `/v1/customers` | Create customer | `customers()->create()` |
| GET | `/v1/customers/{id}` | Retrieve customer | `customers()->get()` |
| PUT | `/v1/customers/{id}` | Update customer | `customers()->update()` |
| DELETE | `/v1/customers/{id}` | Delete customer | `customers()->delete()` |
| GET | `/v1/customers` | List customers | `customers()->list()` |
| POST | `/v1/customers/{id}/payment_methods` | Add payment method to customer | `customers()->addPaymentMethod()` |
| GET | `/v1/customers/{id}/payment_methods` | List customer payment methods | `customers()->listPaymentMethods()` |
| DELETE | `/v1/customers/{id}/payment_methods/{pmId}` | Delete customer payment method | `customers()->deletePaymentMethod()` |
| POST | `/v1/checkout` | Create checkout page | `checkout()->create()` |
| GET | `/v1/checkout/{id}` | Retrieve checkout page | `checkout()->get()` |
| POST | `/v1/hosted/collect/payments` | Create payment link | `paymentLinks()->create()` |
| GET | `/v1/hosted/collect/payments/{id}` | Retrieve payment link | `paymentLinks()->get()` |
| GET | `/v1/hosted/collect/payments` | List payment links | `paymentLinks()->list()` |
| GET | `/v1/payment_methods/country?country={cc}` | List payment methods by country | `paymentMethods()->listByCountry()` |
| GET | `/v1/payment_methods/{type}/required_fields` | Get required fields | `paymentMethods()->requiredFields()` |
| POST | `/v1/subscriptions` | Create subscription | `subscriptions()->create()` |
| GET | `/v1/subscriptions/{id}` | Retrieve subscription | `subscriptions()->get()` |
| PUT | `/v1/subscriptions/{id}` | Update subscription | `subscriptions()->update()` |
| DELETE | `/v1/subscriptions/{id}` | Cancel subscription | `subscriptions()->cancel()` |
| GET | `/v1/subscriptions` | List subscriptions | `subscriptions()->list()` |
| POST | `/v1/plans` | Create plan | `plans()->create()` |
| GET | `/v1/plans/{id}` | Retrieve plan | `plans()->get()` |
| PUT | `/v1/plans/{id}` | Update plan | `plans()->update()` |
| DELETE | `/v1/plans/{id}` | Delete plan | `plans()->delete()` |
| GET | `/v1/plans` | List plans | `plans()->list()` |
| POST | `/v1/products` | Create product | `products()->create()` |
| GET | `/v1/products/{id}` | Retrieve product | `products()->get()` |
| PUT | `/v1/products/{id}` | Update product | `products()->update()` |
| DELETE | `/v1/products/{id}` | Delete product | `products()->delete()` |
| GET | `/v1/products` | List products | `products()->list()` |
| POST | `/v1/invoices` | Create invoice | `invoices()->create()` |
| GET | `/v1/invoices/{id}` | Retrieve invoice | `invoices()->get()` |
| PUT | `/v1/invoices/{id}` | Update invoice | `invoices()->update()` |
| DELETE | `/v1/invoices/{id}` | Delete invoice | `invoices()->delete()` |
| GET | `/v1/invoices` | List invoices | `invoices()->list()` |
| POST | `/v1/invoices/{id}/finalize` | Finalize invoice | `invoices()->finalize()` |
| POST | `/v1/invoices/{id}/pay` | Pay invoice | `invoices()->pay()` |
| GET | `/v1/payment_disputes/{id}` | Retrieve dispute | `disputes()->get()` |
| GET | `/v1/payment_disputes` | List disputes | `disputes()->list()` |
| POST | `/v1/escrows/{id}/escrow_releases` | Release escrow | `escrows()->release()` |

### 3.2 Disburse (Payouts)

| Method | Path | Description | Resource Method |
|---|---|---|---|
| POST | `/v1/payouts` | Create payout | `payouts()->create()` |
| GET | `/v1/payouts/{id}` | Retrieve payout | `payouts()->get()` |
| PUT | `/v1/payouts/{id}` | Update payout | `payouts()->update()` |
| DELETE | `/v1/payouts/{id}` | Cancel payout | `payouts()->cancel()` |
| GET | `/v1/payouts` | List payouts | `payouts()->list()` |
| POST | `/v1/payouts/confirm/{id}` | Confirm payout | `payouts()->confirm()` |
| POST | `/v1/payouts/complete/{id}/{amount}` | Complete payout (sandbox) | `payouts()->complete()` |
| POST | `/v1/payouts/{id}/beneficiary/response` | Set payout response | `payouts()->setResponse()` |
| GET | `/v1/payouts/{id}/payout_method_types` | List payout method types | `payoutMethods()->listTypes()` |
| GET | `/v1/payout_method_types` | List all payout method types | `payoutMethods()->list()` |
| GET | `/v1/payouts/required_fields/{type}` | Get required fields | `payoutMethods()->requiredFields()` |
| POST | `/v1/payouts/beneficiary` | Create beneficiary | `beneficiaries()->create()` |
| GET | `/v1/payouts/beneficiary/{id}` | Retrieve beneficiary | `beneficiaries()->get()` |
| PUT | `/v1/payouts/beneficiary/{id}` | Update beneficiary | `beneficiaries()->update()` |
| DELETE | `/v1/payouts/beneficiary/{id}` | Delete beneficiary | `beneficiaries()->delete()` |
| GET | `/v1/payouts/beneficiary` | List beneficiaries | `beneficiaries()->list()` |
| POST | `/v1/payouts/sender` | Create sender | `senders()->create()` |
| GET | `/v1/payouts/sender/{id}` | Retrieve sender | `senders()->get()` |
| PUT | `/v1/payouts/sender/{id}` | Update sender | `senders()->update()` |
| DELETE | `/v1/payouts/sender/{id}` | Delete sender | `senders()->delete()` |
| GET | `/v1/payouts/sender` | List senders | `senders()->list()` |

### 3.3 Wallet

| Method | Path | Description | Resource Method |
|---|---|---|---|
| POST | `/v1/user` | Create wallet | `wallets()->create()` |
| GET | `/v1/user/{id}` | Retrieve wallet | `wallets()->get()` |
| PUT | `/v1/user/{id}` | Update wallet | `wallets()->update()` |
| DELETE | `/v1/user/{id}` | Delete wallet | `wallets()->delete()` |
| GET | `/v1/user` | List wallets | `wallets()->list()` |
| POST | `/v1/user/{id}/contacts` | Add contact to wallet | `walletContacts()->create()` |
| GET | `/v1/user/{walletId}/contacts/{contactId}` | Retrieve contact | `walletContacts()->get()` |
| PUT | `/v1/user/{walletId}/contacts/{contactId}` | Update contact | `walletContacts()->update()` |
| DELETE | `/v1/user/{walletId}/contacts/{contactId}` | Delete contact | `walletContacts()->delete()` |
| GET | `/v1/user/{id}/contacts` | List contacts | `walletContacts()->list()` |
| POST | `/v1/account/transfer` | Transfer between wallets | `walletTransfers()->create()` |
| PUT | `/v1/account/transfer/response` | Set transfer response | `walletTransfers()->setResponse()` |
| GET | `/v1/user/{id}/transactions` | List transactions | `walletTransactions()->list()` |
| GET | `/v1/user/{walletId}/transactions/{transactionId}` | Retrieve transaction | `walletTransactions()->get()` |
| POST | `/v1/virtual_accounts` | Issue virtual account | `virtualAccounts()->create()` |
| GET | `/v1/virtual_accounts/{id}` | Retrieve virtual account | `virtualAccounts()->get()` |
| PUT | `/v1/virtual_accounts/{id}` | Update virtual account | `virtualAccounts()->update()` |
| DELETE | `/v1/virtual_accounts/{id}` | Close virtual account | `virtualAccounts()->close()` |
| GET | `/v1/virtual_accounts` | List virtual accounts | `virtualAccounts()->list()` |

### 3.4 Issuing (Cards)

| Method | Path | Description | Resource Method |
|---|---|---|---|
| POST | `/v1/issuing/cards` | Issue card | `cards()->create()` |
| GET | `/v1/issuing/cards/{id}` | Retrieve card | `cards()->get()` |
| PUT | `/v1/issuing/cards/{id}` | Update card | `cards()->update()` |
| POST | `/v1/issuing/cards/status` | Update card status | `cards()->updateStatus()` |
| POST | `/v1/issuing/cards/activate` | Activate card | `cards()->activate()` |
| GET | `/v1/issuing/cards` | List cards | `cards()->list()` |
| GET | `/v1/issuing/cards/{id}/transactions` | List card transactions | `cards()->listTransactions()` |
| POST | `/v1/issuing/cards/pin/set` | Set PIN | `cards()->setPin()` |
| GET | `/v1/issuing/cards/pin/get` | Get PIN | `cards()->getPin()` |
| POST | `/v1/issuing/card_programs` | Create card program | `cardPrograms()->create()` |
| GET | `/v1/issuing/card_programs/{id}` | Retrieve card program | `cardPrograms()->get()` |
| GET | `/v1/issuing/card_programs` | List card programs | `cardPrograms()->list()` |

### 3.5 Verify (KYC/KYB)

| Method | Path | Description | Resource Method |
|---|---|---|---|
| POST | `/v1/identities` | Create identity verification | `identities()->create()` |
| GET | `/v1/identities/{id}` | Retrieve identity | `identities()->get()` |
| GET | `/v1/identities` | List identities | `identities()->list()` |
| POST | `/v1/hosted/idv` | Create verification hosted page | `verification()->createHostedPage()` |
| GET | `/v1/verify/applications/status/{id}` | Get application status | `verification()->getApplicationStatus()` |

### 3.6 Protect (Fraud)

| Method | Path | Description | Resource Method |
|---|---|---|---|
| GET | `/v1/fraud/merchant/settings` | Get fraud settings | `fraud()->getSettings()` |
| PUT | `/v1/fraud/merchant/settings` | Update fraud settings | `fraud()->updateSettings()` |

### 3.7 Data / Utilities

| Method | Path | Description | Resource Method |
|---|---|---|---|
| GET | `/v1/data/countries` | List countries | `data()->countries()` |
| GET | `/v1/data/currencies` | List currencies | `data()->currencies()` |
| GET | `/v1/rates/fxrate` | Get FX rate | `data()->fxRate()` |
| GET | `/v1/rates/daily` | Get daily rate | `data()->dailyRate()` |

---

## 4. Complete Webhook Event Types

The SDK must register a Laravel Event class for every webhook type. Webhook `type` field values:

### 4.1 Payment Webhooks
- `PAYMENT_COMPLETED` — Payment is fully completed (funds captured)
- `PAYMENT_SUCCEEDED` — Payment succeeded (synchronous, same as response)
- `PAYMENT_FAILED` — Payment failed
- `PAYMENT_EXPIRED` — Payment expired before completion
- `PAYMENT_UPDATED` — Payment object was modified
- `PAYMENT_CAPTURED` — Auth-only payment was captured
- `PAYMENT_CANCELED` — Payment was canceled
- `PAYMENT_REFUND_COMPLETED` — Refund on a payment completed
- `PAYMENT_REFUND_FAILED` — Refund on a payment failed
- `PAYMENT_REFUND_REJECTED` — Refund was rejected by processor
- `PAYMENT_DISPUTE_CREATED` — Dispute was created
- `PAYMENT_DISPUTE_UPDATED` — Dispute status changed

### 4.2 Refund Webhooks
- `REFUND_COMPLETED` — Standalone refund completed
- `REFUND_FAILED` — Standalone refund failed
- `REFUND_REJECTED` — Standalone refund rejected

### 4.3 Customer Webhooks
- `CUSTOMER_CREATED` — Customer object created
- `CUSTOMER_UPDATED` — Customer object updated
- `CUSTOMER_DELETED` — Customer object deleted
- `CUSTOMER_PAYMENT_METHOD_CREATED` — Payment method added to customer
- `CUSTOMER_PAYMENT_METHOD_UPDATED` — Customer payment method updated
- `CUSTOMER_PAYMENT_METHOD_DELETED` — Customer payment method deleted
- `CUSTOMER_PAYMENT_METHOD_EXPIRING` — Customer payment method nearing expiry

### 4.4 Subscription Webhooks
- `CUSTOMER_SUBSCRIPTION_CREATED` — Subscription created
- `CUSTOMER_SUBSCRIPTION_UPDATED` — Subscription updated
- `CUSTOMER_SUBSCRIPTION_COMPLETED` — Subscription billing cycle completed
- `CUSTOMER_SUBSCRIPTION_CANCELED` — Subscription canceled
- `CUSTOMER_SUBSCRIPTION_PAST_DUE` — Subscription payment overdue
- `CUSTOMER_SUBSCRIPTION_TRIAL_END` — Subscription trial period ending
- `CUSTOMER_SUBSCRIPTION_RENEWED` — Subscription renewed

### 4.5 Invoice Webhooks
- `INVOICE_CREATED` — Invoice created
- `INVOICE_UPDATED` — Invoice updated
- `INVOICE_PAYMENT_CREATED` — Payment created for invoice
- `INVOICE_PAYMENT_SUCCEEDED` — Invoice payment succeeded
- `INVOICE_PAYMENT_FAILED` — Invoice payment failed

### 4.6 Payout Webhooks
- `PAYOUT_COMPLETED` — Payout fully completed
- `PAYOUT_UPDATED` — Payout object was updated
- `PAYOUT_FAILED` — Payout failed
- `PAYOUT_EXPIRED` — Payout expired
- `PAYOUT_CANCELED` — Payout was canceled
- `PAYOUT_RETURNED` — Payout was returned (beneficiary rejected)

### 4.7 Wallet Webhooks
- `WALLET_TRANSACTION` — Wallet transaction occurred
- `WALLET_FUNDS_ADDED` — Funds added to wallet
- `WALLET_FUNDS_REMOVED` — Funds removed from wallet
- `WALLET_TRANSFER_COMPLETED` — Transfer between wallets completed
- `WALLET_TRANSFER_FAILED` — Transfer between wallets failed
- `WALLET_TRANSFER_RESPONSE_RECEIVED` — Transfer response from beneficiary wallet

### 4.8 Card Issuing Webhooks
- `CARD_ISSUING_AUTHORIZATION_APPROVED` — Card transaction authorization approved
- `CARD_ISSUING_AUTHORIZATION_DECLINED` — Card transaction authorization declined
- `CARD_ISSUING_SALE` — Card sale completed
- `CARD_ISSUING_CREDIT` — Credit issued to card
- `CARD_ISSUING_REVERSAL` — Card transaction reversed
- `CARD_ISSUING_REFUND` — Refund to issued card
- `CARD_ISSUING_CHARGEBACK` — Chargeback on issued card
- `CARD_ISSUING_ADJUSTMENT` — Adjustment to card transaction
- `CARD_ISSUING_ATM_FEE` — ATM fee charged
- `CARD_ISSUING_ATM_WITHDRAWAL` — ATM withdrawal
- `CARD_ADDED_SUCCESSFULLY` — Card added successfully to customer
- `CARD_ISSUING_TRANSACTION_COMPLETED` — Card transaction fully completed

### 4.9 Verify/KYC Webhooks
- `VERIFY_APPLICATION_SUBMITTED` — KYC application submitted
- `VERIFY_APPLICATION_APPROVED` — KYC application approved
- `VERIFY_APPLICATION_REJECTED` — KYC application rejected

### 4.10 Virtual Account Webhooks
- `VIRTUAL_ACCOUNT_CREATED` — Virtual account created
- `VIRTUAL_ACCOUNT_UPDATED` — Virtual account updated
- `VIRTUAL_ACCOUNT_CLOSED` — Virtual account closed
- `VIRTUAL_ACCOUNT_TRANSACTION` — Transaction on virtual account

---

## 5. Enum Definitions

All enums go in `src/Enums/`. Use PHP 8.1+ backed enums with `string` backing type.

### 5.1 PaymentStatus
```php
enum PaymentStatus: string {
    case Active = 'ACT';        // Awaiting completion/3DS/capture
    case Closed = 'CLO';        // Payment completed successfully
    case Canceled = 'CAN';      // Canceled by client or customer bank
    case Error = 'ERR';         // Payment processing error
    case Expired = 'EXP';       // Payment expired
    case Reviewed = 'REV';      // Payment under review
    case New = 'NEW';           // Payment newly created
}
```

### 5.2 PaymentMethodCategory
```php
enum PaymentMethodCategory: string {
    case Card = 'card';
    case Cash = 'cash';
    case BankTransfer = 'bank_transfer';
    case BankRedirect = 'bank_redirect';
    case EWallet = 'ewallet';
}
```

### 5.3 PaymentFlowType
```php
enum PaymentFlowType: string {
    case Direct = 'direct';
    case Redirect = 'redirect';
    case EWalletPayer = 'ewallet_payer';
}
```

### 5.4 NextAction
```php
enum NextAction: string {
    case ThreeDSVerification = '3d_verification';
    case PendingConfirmation = 'pending_confirmation';
    case PendingCapture = 'pending_capture';
    case NotApplicable = 'not_applicable';
}
```

### 5.5 RefundStatus
```php
enum RefundStatus: string {
    case Pending = 'Pending';
    case Completed = 'Completed';
    case Canceled = 'Canceled';
    case Error = 'Error';
    case Rejected = 'Rejected';
}
```

### 5.6 DisputeStatus
```php
enum DisputeStatus: string {
    case Active = 'ACT';
    case Review = 'RVW';
    case PreArbitration = 'PRA';
    case Arbitration = 'ARB';
    case Loss = 'LOS';
    case Win = 'WIN';
    case Reverse = 'REV';
}
```

### 5.7 PayoutStatus
```php
enum PayoutStatus: string {
    case Created = 'Created';
    case Confirmation = 'Confirmation';
    case Completed = 'Completed';
    case Canceled = 'Canceled';
    case Error = 'Error';
    case Expired = 'Expired';
    case Returned = 'Returned';
}
```

### 5.8 PayoutMethodCategory
```php
enum PayoutMethodCategory: string {
    case Bank = 'bank';
    case Cash = 'cash';
    case Card = 'card';
    case EWallet = 'ewallet';
    case RapydWallet = 'rapyd_ewallet';
}
```

### 5.9 SubscriptionStatus
```php
enum SubscriptionStatus: string {
    case Active = 'active';
    case Canceled = 'canceled';
    case PastDue = 'past_due';
    case Trialing = 'trialing';
    case Unpaid = 'unpaid';
}
```

### 5.10 InvoiceStatus
```php
enum InvoiceStatus: string {
    case Draft = 'draft';
    case Open = 'open';
    case Paid = 'paid';
    case Uncollectible = 'uncollectible';
    case Void = 'void';
}
```

### 5.11 WebhookStatus
```php
enum WebhookStatus: string {
    case New = 'NEW';
    case ReSent = 'RET';
    case Closed = 'CLO';
    case Error = 'ERR';
}
```

### 5.12 CardStatus
```php
enum CardStatus: string {
    case Active = 'ACT';
    case Inactive = 'INA';
    case Blocked = 'BLO';
    case Expired = 'EXP';
}
```

### 5.13 CardBlockReasonCode
```php
enum CardBlockReasonCode: string {
    case Stolen = 'STO';
    case Lost = 'LOS';
    case Fraud = 'FRD';
    case Canceled = 'CAN';
    case Locked = 'LOC';  // Incorrect PIN
}
```

### 5.14 EntityType
```php
enum EntityType: string {
    case Individual = 'individual';
    case Company = 'company';
}
```

### 5.15 FeeCalcType
```php
enum FeeCalcType: string {
    case Net = 'net';
    case Gross = 'gross';
}
```

### 5.16 FixedSide
```php
enum FixedSide: string {
    case Buy = 'buy';
    case Sell = 'sell';
}
```

### 5.17 WalletContactType
```php
enum WalletContactType: string {
    case Personal = 'personal';
    case Business = 'business';
}
```

### 5.18 CouponDuration
```php
enum CouponDuration: string {
    case Forever = 'forever';
    case Repeating = 'repeating';
    case Once = 'once';
}
```

### 5.19 PlanInterval
```php
enum PlanInterval: string {
    case Day = 'day';
    case Week = 'week';
    case Month = 'month';
    case Year = 'year';
}
```

### 5.20 CheckoutPageStatus
```php
enum CheckoutPageStatus: string {
    case New = 'NEW';
    case Done = 'DON';
    case Expired = 'EXP';
}
```

### 5.21 EscrowStatus
```php
enum EscrowStatus: string {
    case Pending = 'pending';
    case Released = 'released';
    case PartiallyReleased = 'partially_released';
}
```

### 5.22 IssuingTxnType
```php
enum IssuingTxnType: string {
    case Sale = 'SALE';
    case Credit = 'CREDIT';
    case Reversal = 'REVERSAL';
    case Refund = 'REFUND';
    case Chargeback = 'CHARGEBACK';
    case Adjustment = 'ADJUSTMENT';
    case AtmFee = 'ATM_FEE';
    case AtmWithdrawal = 'ATM_WITHDRAWAL';
}
```

### 5.23 Environment
```php
enum Environment: string {
    case Sandbox = 'sandbox';
    case Production = 'production';
}
```

### 5.24 WebhookEventType
```php
// This is the master enum for ALL webhook types.
// Use for the webhook dispatcher switch and event mapping.
enum WebhookEventType: string {
    // Payments
    case PaymentCompleted = 'PAYMENT_COMPLETED';
    case PaymentSucceeded = 'PAYMENT_SUCCEEDED';
    case PaymentFailed = 'PAYMENT_FAILED';
    case PaymentExpired = 'PAYMENT_EXPIRED';
    case PaymentUpdated = 'PAYMENT_UPDATED';
    case PaymentCaptured = 'PAYMENT_CAPTURED';
    case PaymentCanceled = 'PAYMENT_CANCELED';
    case PaymentRefundCompleted = 'PAYMENT_REFUND_COMPLETED';
    case PaymentRefundFailed = 'PAYMENT_REFUND_FAILED';
    case PaymentRefundRejected = 'PAYMENT_REFUND_REJECTED';
    case PaymentDisputeCreated = 'PAYMENT_DISPUTE_CREATED';
    case PaymentDisputeUpdated = 'PAYMENT_DISPUTE_UPDATED';
    // Refunds
    case RefundCompleted = 'REFUND_COMPLETED';
    case RefundFailed = 'REFUND_FAILED';
    case RefundRejected = 'REFUND_REJECTED';
    // Customers
    case CustomerCreated = 'CUSTOMER_CREATED';
    case CustomerUpdated = 'CUSTOMER_UPDATED';
    case CustomerDeleted = 'CUSTOMER_DELETED';
    case CustomerPaymentMethodCreated = 'CUSTOMER_PAYMENT_METHOD_CREATED';
    case CustomerPaymentMethodUpdated = 'CUSTOMER_PAYMENT_METHOD_UPDATED';
    case CustomerPaymentMethodDeleted = 'CUSTOMER_PAYMENT_METHOD_DELETED';
    case CustomerPaymentMethodExpiring = 'CUSTOMER_PAYMENT_METHOD_EXPIRING';
    // Subscriptions
    case SubscriptionCreated = 'CUSTOMER_SUBSCRIPTION_CREATED';
    case SubscriptionUpdated = 'CUSTOMER_SUBSCRIPTION_UPDATED';
    case SubscriptionCompleted = 'CUSTOMER_SUBSCRIPTION_COMPLETED';
    case SubscriptionCanceled = 'CUSTOMER_SUBSCRIPTION_CANCELED';
    case SubscriptionPastDue = 'CUSTOMER_SUBSCRIPTION_PAST_DUE';
    case SubscriptionTrialEnd = 'CUSTOMER_SUBSCRIPTION_TRIAL_END';
    case SubscriptionRenewed = 'CUSTOMER_SUBSCRIPTION_RENEWED';
    // Invoices
    case InvoiceCreated = 'INVOICE_CREATED';
    case InvoiceUpdated = 'INVOICE_UPDATED';
    case InvoicePaymentCreated = 'INVOICE_PAYMENT_CREATED';
    case InvoicePaymentSucceeded = 'INVOICE_PAYMENT_SUCCEEDED';
    case InvoicePaymentFailed = 'INVOICE_PAYMENT_FAILED';
    // Payouts
    case PayoutCompleted = 'PAYOUT_COMPLETED';
    case PayoutUpdated = 'PAYOUT_UPDATED';
    case PayoutFailed = 'PAYOUT_FAILED';
    case PayoutExpired = 'PAYOUT_EXPIRED';
    case PayoutCanceled = 'PAYOUT_CANCELED';
    case PayoutReturned = 'PAYOUT_RETURNED';
    // Wallet
    case WalletTransaction = 'WALLET_TRANSACTION';
    case WalletFundsAdded = 'WALLET_FUNDS_ADDED';
    case WalletFundsRemoved = 'WALLET_FUNDS_REMOVED';
    case WalletTransferCompleted = 'WALLET_TRANSFER_COMPLETED';
    case WalletTransferFailed = 'WALLET_TRANSFER_FAILED';
    case WalletTransferResponseReceived = 'WALLET_TRANSFER_RESPONSE_RECEIVED';
    // Card Issuing
    case CardIssuingAuthApproved = 'CARD_ISSUING_AUTHORIZATION_APPROVED';
    case CardIssuingAuthDeclined = 'CARD_ISSUING_AUTHORIZATION_DECLINED';
    case CardIssuingSale = 'CARD_ISSUING_SALE';
    case CardIssuingCredit = 'CARD_ISSUING_CREDIT';
    case CardIssuingReversal = 'CARD_ISSUING_REVERSAL';
    case CardIssuingRefund = 'CARD_ISSUING_REFUND';
    case CardIssuingChargeback = 'CARD_ISSUING_CHARGEBACK';
    case CardIssuingAdjustment = 'CARD_ISSUING_ADJUSTMENT';
    case CardIssuingAtmFee = 'CARD_ISSUING_ATM_FEE';
    case CardIssuingAtmWithdrawal = 'CARD_ISSUING_ATM_WITHDRAWAL';
    case CardAddedSuccessfully = 'CARD_ADDED_SUCCESSFULLY';
    case CardIssuingTxnCompleted = 'CARD_ISSUING_TRANSACTION_COMPLETED';
    // Verify
    case VerifyApplicationSubmitted = 'VERIFY_APPLICATION_SUBMITTED';
    case VerifyApplicationApproved = 'VERIFY_APPLICATION_APPROVED';
    case VerifyApplicationRejected = 'VERIFY_APPLICATION_REJECTED';
    // Virtual Accounts
    case VirtualAccountCreated = 'VIRTUAL_ACCOUNT_CREATED';
    case VirtualAccountUpdated = 'VIRTUAL_ACCOUNT_UPDATED';
    case VirtualAccountClosed = 'VIRTUAL_ACCOUNT_CLOSED';
    case VirtualAccountTransaction = 'VIRTUAL_ACCOUNT_TRANSACTION';
}
```

---

---

## 6. Implementation Flows

### 6.1 Basic Card Payment Flow

```
1. List payment methods for country:
   GET /v1/payment_methods/country?country=US

2. Get required fields for the payment method:
   GET /v1/payment_methods/us_visa_card/required_fields

3. Create a customer (optional, for recurring):
   POST /v1/customers
   Body: { "name": "John Doe", "email": "john@example.com" }

4. Create the payment:
   POST /v1/payments
   Body: {
     "amount": 100.00,
     "currency": "USD",
     "payment_method": {
       "type": "us_visa_card",
       "fields": {
         "number": "4111111111111111",
         "expiration_month": "12",
         "expiration_year": "29",
         "cvv": "345",
         "name": "John Doe"
       }
     },
     "capture": true
   }

5. Handle 3DS if required:
   - Check response: payment.next_action == "3d_verification"
   - Redirect customer to: payment.redirect_url
   - Customer completes 3DS challenge
   - Rapyd redirects back to complete_payment_url

6. Receive webhook:
   PAYMENT_COMPLETED (payment.status == "CLO")
```

### 6.2 Hosted Checkout Flow (No PCI Required)

```
1. Create a checkout page:
   POST /v1/checkout
   Body: {
     "amount": 100,
     "country": "US",
     "currency": "USD",
     "complete_checkout_url": "https://yoursite.com/success",
     "error_payment_url": "https://yoursite.com/error",
     "payment_method_types_include": ["us_visa_card", "us_mastercard_card"]
   }

2. Redirect customer to: response.data.redirect_url

3. Customer selects payment method and pays on Rapyd's hosted page

4. Rapyd redirects customer to complete_checkout_url or error_payment_url

5. Receive webhook: PAYMENT_COMPLETED
```

### 6.3 Payout (Disbursement) Flow

```
1. List payout methods for the target country:
   GET /v1/payouts/supported_types?beneficiary_country=PH&payout_currency=PHP&category=bank

2. Get required fields for the payout method:
   GET /v1/payouts/required_fields/ph_metrobank_bank

3. Create a beneficiary (the person receiving money):
   POST /v1/payouts/beneficiary
   Body: {
     "category": "bank",
     "country": "PH",
     "currency": "PHP",
     "entity_type": "individual",
     "first_name": "Maria",
     "last_name": "Santos",
     "identification_type": "work_permit",
     "identification_value": "1234567890",
     "account_number": "1234567890",
     "bank_name": "Metrobank"
   }

4. Create a sender (the entity sending money):
   POST /v1/payouts/sender
   Body: {
     "country": "US",
     "currency": "USD",
     "entity_type": "company",
     "company_name": "Your Company Inc.",
     "identification_type": "company_registered_number",
     "identification_value": "12-3456789"
   }

5. Create the payout:
   POST /v1/payouts
   Body: {
     "beneficiary": "beneficiary_id",
     "sender": "sender_id",
     "payout_amount": 10000,
     "payout_currency": "PHP",
     "payout_method_type": "ph_metrobank_bank",
     "ewallet": "ewallet_your_company_wallet_id",
     "sender_currency": "USD",
     "sender_country": "US"
   }

6. If FX is involved and confirm_automatically is false:
   POST /v1/payouts/confirm/{payout_id}

7. Receive webhook: PAYOUT_COMPLETED or PAYOUT_FAILED
```

### 6.4 Subscription Flow

```
1. Create a product:
   POST /v1/products
   Body: { "name": "Pro Plan", "type": "service" }

2. Create a plan:
   POST /v1/plans
   Body: {
     "product": "product_id",
     "amount": 29.99,
     "currency": "USD",
     "interval": "month",
     "billing_scheme": "per_unit"
   }

3. Create a customer with a payment method:
   POST /v1/customers
   Body: {
     "name": "John Doe",
     "email": "john@example.com",
     "payment_method": {
       "type": "us_visa_card",
       "fields": { ... }
     }
   }

4. Create a subscription:
   POST /v1/subscriptions
   Body: {
     "customer": "cus_id",
     "billing": "pay_automatically",
     "subscription_items": [
       { "plan": "plan_id", "quantity": 1 }
     ]
   }

5. Rapyd automatically charges on each billing cycle
6. Webhooks: CUSTOMER_SUBSCRIPTION_CREATED, INVOICE_PAYMENT_SUCCEEDED
```

### 6.5 Wallet Transfer Flow

```
1. Create wallets for both parties:
   POST /v1/user (for sender and receiver)

2. Fund the sender wallet:
   POST /v1/payments (with ewallet_id of sender)

3. Transfer between wallets:
   POST /v1/account/transfer
   Body: {
     "source_ewallet": "ewallet_sender_id",
     "destination_ewallet": "ewallet_receiver_id",
     "amount": 500,
     "currency": "USD"
   }

4. If confirmation required:
   PUT /v1/account/transfer/response
   Body: { "id": "transfer_id", "status": "accept" }

5. Webhooks: WALLET_TRANSFER_COMPLETED
```

### 6.6 Card Issuing Flow

```
1. Create or use an existing card program:
   POST /v1/issuing/card_programs
   GET /v1/issuing/card_programs

2. Issue a card:
   POST /v1/issuing/cards
   Body: {
     "ewallet_contact": "cont_contact_id",
     "card_program": "cardprog_id"
   }

3. Activate the card:
   POST /v1/issuing/cards/activate
   Body: { "card": "card_id" }

4. Set PIN:
   POST /v1/issuing/cards/pin/set
   Body: { "card": "card_id", "pin": "1234" }

5. Monitor transactions via webhooks:
   CARD_ISSUING_AUTHORIZATION_APPROVED
   CARD_ISSUING_SALE
   CARD_ISSUING_TRANSACTION_COMPLETED
```

---

## 7. Sandbox Testing

### 7.1 Base URL
```
https://sandboxapi.rapyd.net
```

### 7.2 Test Card Numbers

| Card Number | Behavior |
|-------------|----------|
| `4111111111111111` | Visa — successful payment |
| `5555555555554444` | Mastercard — successful payment |
| `4000000000000077` | Visa — 3DS required |
| `4000000000000002` | Visa — card declined |
| `4000000000000069` | Visa — expired card |

CVV: any 3 digits. Expiration: any future date.

### 7.3 Simulating Payment Completion
In sandbox, some payment methods require completing via:
```
POST /v1/payments/completePayment/{payment_id}/{amount}
```

### 7.4 Simulating Payout Completion
```
POST /v1/payouts/complete/{payout_id}/{amount}
```

### 7.5 Error Simulation
Add `"error_payment_url"` and specific metadata to trigger test errors.

### 7.6 Webhook Testing
- Sandbox generates real webhooks
- Use ngrok or a similar tool to expose local endpoints
- Webhook endpoint configured in Client Portal → Developers → Webhooks
- Sandbox authentication code for Rapyd Verify: `111111`

---

## 8. Pagination

List endpoints support pagination via query parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `limit` | Number of results per page | 10 |
| `page` | Page number (1-indexed) | 1 |
| `starting_after` | ID of object created before the first result you want | — |
| `ending_before` | ID of object created after the last result you want | — |

Response includes pagination hints — check if `data` array length equals `limit` to determine if more pages exist.

---

## 9. Error Handling

### 9.1 Error Response Format
```json
{
  "status": {
    "error_code": "INVALID_FIELDS",
    "status": "ERROR",
    "message": "The request tried to create an object, but one or more of the fields has an error.",
    "response_code": "INVALID_FIELDS",
    "operation_id": "uuid-here"
  }
}
```

### 9.2 Common Error Codes

| Error Code | Meaning |
|-----------|---------|
| `UNAUTHORIZED_API_CALL` | Invalid access key or signature |
| `INVALID_FIELDS` | Required field missing or invalid value |
| `NOT_FOUND` | Object with the specified ID doesn't exist |
| `INVALID_BODY` | Request body is malformed JSON |
| `DUPLICATE_ENTRY` | Idempotency key was reused |
| `UNAUTHENTICATED` | Invalid or expired signature/timestamp |
| `INSUFFICIENT_FUNDS` | Wallet doesn't have enough balance |
| `PAYMENT_METHOD_NOT_SUPPORTED` | Payment method not available in country |
| `GENERAL_ERROR` | Catch-all server error |

### 9.3 Rate Limiting
Rapyd applies rate limits per access key. If exceeded, you receive HTTP 429. Implement exponential backoff with retry.

---

## 10. Currency & Country Codes

### Supported Settlement Currencies (partial list)
USD, EUR, GBP, GEL, MXN, THB, AUD, MYR, TRY, BGN, NGN, NOK, BRL, GTQ, PHP, CAD, HUF, PLN, CHF, IDR, RON, CLP, JPY, SEK, CNY, KES, SGD, COP, KRW, ZAR, CZK, DKK, INR, ILS, HKD, AED, SAR, BHD, KWD, NZD, TWD

### Country Codes (examples)
US, GB, DE, FR, GE (Georgia), PH (Philippines), NG (Nigeria), BR (Brazil), PL (Poland), TR (Turkey), IN (India), ID (Indonesia), SG (Singapore), JP (Japan), AU (Australia), MX (Mexico)

Use `GET /v1/data/countries` and `GET /v1/data/currencies` for complete lists.

---

## 11. ID Prefixes

Every Rapyd object has a prefixed ID:

| Prefix | Object |
|--------|--------|
| `payment_` | Payment |
| `refund_` | Refund |
| `cus_` | Customer |
| `card_` | Card payment method |
| `other_` | Non-card payment method |
| `checkout_` | Checkout page |
| `sub_` | Subscription |
| `plan_` | Plan |
| `product_` | Product |
| `invoice_` | Invoice |
| `payout_` | Payout |
| `beneficiary_` | Beneficiary |
| `sender_` | Sender |
| `ewallet_` | Wallet |
| `cont_` | Wallet contact |
| `wt_` | Wallet transaction |
| `card_` (issuing) | Issued card |
| `cardprog_` | Card program |
| `cardauth_` | Card authorization |
| `cit_` | Card issuing transaction |
| `wh_` | Webhook |
| `happ_` | Hosted application |
| `app_` | Verify application |

---

## 12. Related Resources

- **Official Docs**: https://docs.rapyd.net
- **API Reference**: https://docs.rapyd.net/en/merchant-api-reference.html
- **Client Portal (Sandbox)**: https://dashboard.rapyd.net
- **Community Forum**: https://community.rapyd.net
- **OpenAPI Spec**: https://github.com/Rapyd-Samples/RapydOpenAPI
- **Laravel SDK**: https://github.com/saba-ab/rapyd (Packagist: saba-ab/rapyd)
- **Contact**: community@rapyd.net, support@rapyd.net
