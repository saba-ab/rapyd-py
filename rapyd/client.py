"""RapydClient — main entry point for the Rapyd Python SDK."""

from __future__ import annotations

from rapyd.config import RapydSettings
from rapyd.http import RapydHttpClient
from rapyd.resources.beneficiaries import BeneficiariesResource
from rapyd.resources.card_programs import CardProgramsResource
from rapyd.resources.cards import CardsResource
from rapyd.resources.checkout import CheckoutResource
from rapyd.resources.customers import CustomersResource
from rapyd.resources.data import DataResource
from rapyd.resources.disputes import DisputesResource
from rapyd.resources.fraud import FraudResource
from rapyd.resources.identities import IdentitiesResource
from rapyd.resources.invoices import InvoicesResource
from rapyd.resources.payment_links import PaymentLinksResource
from rapyd.resources.payment_methods import PaymentMethodsResource
from rapyd.resources.payments import PaymentsResource
from rapyd.resources.payout_methods import PayoutMethodsResource
from rapyd.resources.payouts import PayoutsResource
from rapyd.resources.plans import PlansResource
from rapyd.resources.products import ProductsResource
from rapyd.resources.refunds import RefundsResource
from rapyd.resources.senders import SendersResource
from rapyd.resources.subscriptions import SubscriptionsResource
from rapyd.resources.verification import VerificationResource
from rapyd.resources.virtual_accounts import VirtualAccountsResource
from rapyd.resources.wallet_contacts import WalletContactsResource
from rapyd.resources.wallet_transactions import WalletTransactionsResource
from rapyd.resources.wallet_transfers import WalletTransfersResource
from rapyd.resources.wallets import WalletsResource


class RapydClient:
    """Async client for the Rapyd Fintech-as-a-Service API.

    Usage::

        async with RapydClient() as rapyd:
            payment = await rapyd.payments().get("payment_xxx")

    Credentials are read from environment variables by default,
    or can be passed explicitly.
    """

    def __init__(
        self,
        *,
        access_key: str | None = None,
        secret_key: str | None = None,
        environment: str = "sandbox",
        timeout: int = 30,
        settings: RapydSettings | None = None,
    ) -> None:
        if settings is not None:
            self._settings = settings
        elif access_key and secret_key:
            self._settings = RapydSettings(
                rapyd_access_key=access_key,
                rapyd_secret_key=secret_key,
                rapyd_environment=environment,  # type: ignore[arg-type]
                rapyd_timeout=timeout,
            )
        else:
            self._settings = RapydSettings()  # type: ignore[call-arg]

        self._http = RapydHttpClient(self._settings)

        # Lazy-cached resource instances
        self._payments: PaymentsResource | None = None
        self._refunds: RefundsResource | None = None
        self._customers: CustomersResource | None = None
        self._checkout: CheckoutResource | None = None
        self._payment_links: PaymentLinksResource | None = None
        self._payment_methods: PaymentMethodsResource | None = None
        self._subscriptions: SubscriptionsResource | None = None
        self._plans: PlansResource | None = None
        self._products: ProductsResource | None = None
        self._invoices: InvoicesResource | None = None
        self._disputes: DisputesResource | None = None
        self._payouts: PayoutsResource | None = None
        self._beneficiaries: BeneficiariesResource | None = None
        self._senders: SendersResource | None = None
        self._payout_methods: PayoutMethodsResource | None = None
        self._wallets: WalletsResource | None = None
        self._wallet_contacts: WalletContactsResource | None = None
        self._wallet_transfers: WalletTransfersResource | None = None
        self._wallet_transactions: WalletTransactionsResource | None = None
        self._virtual_accounts: VirtualAccountsResource | None = None
        self._cards: CardsResource | None = None
        self._card_programs: CardProgramsResource | None = None
        self._identities: IdentitiesResource | None = None
        self._verification: VerificationResource | None = None
        self._fraud: FraudResource | None = None
        self._data: DataResource | None = None

    # --- Resource accessors (lazy, cached) ---

    def payments(self) -> PaymentsResource:
        if self._payments is None:
            self._payments = PaymentsResource(self._http)
        return self._payments

    def refunds(self) -> RefundsResource:
        if self._refunds is None:
            self._refunds = RefundsResource(self._http)
        return self._refunds

    def customers(self) -> CustomersResource:
        if self._customers is None:
            self._customers = CustomersResource(self._http)
        return self._customers

    def checkout(self) -> CheckoutResource:
        if self._checkout is None:
            self._checkout = CheckoutResource(self._http)
        return self._checkout

    def payment_links(self) -> PaymentLinksResource:
        if self._payment_links is None:
            self._payment_links = PaymentLinksResource(self._http)
        return self._payment_links

    def payment_methods(self) -> PaymentMethodsResource:
        if self._payment_methods is None:
            self._payment_methods = PaymentMethodsResource(self._http)
        return self._payment_methods

    def subscriptions(self) -> SubscriptionsResource:
        if self._subscriptions is None:
            self._subscriptions = SubscriptionsResource(self._http)
        return self._subscriptions

    def plans(self) -> PlansResource:
        if self._plans is None:
            self._plans = PlansResource(self._http)
        return self._plans

    def products(self) -> ProductsResource:
        if self._products is None:
            self._products = ProductsResource(self._http)
        return self._products

    def invoices(self) -> InvoicesResource:
        if self._invoices is None:
            self._invoices = InvoicesResource(self._http)
        return self._invoices

    def disputes(self) -> DisputesResource:
        if self._disputes is None:
            self._disputes = DisputesResource(self._http)
        return self._disputes

    def payouts(self) -> PayoutsResource:
        if self._payouts is None:
            self._payouts = PayoutsResource(self._http)
        return self._payouts

    def beneficiaries(self) -> BeneficiariesResource:
        if self._beneficiaries is None:
            self._beneficiaries = BeneficiariesResource(self._http)
        return self._beneficiaries

    def senders(self) -> SendersResource:
        if self._senders is None:
            self._senders = SendersResource(self._http)
        return self._senders

    def payout_methods(self) -> PayoutMethodsResource:
        if self._payout_methods is None:
            self._payout_methods = PayoutMethodsResource(self._http)
        return self._payout_methods

    def wallets(self) -> WalletsResource:
        if self._wallets is None:
            self._wallets = WalletsResource(self._http)
        return self._wallets

    def wallet_contacts(self) -> WalletContactsResource:
        if self._wallet_contacts is None:
            self._wallet_contacts = WalletContactsResource(self._http)
        return self._wallet_contacts

    def wallet_transfers(self) -> WalletTransfersResource:
        if self._wallet_transfers is None:
            self._wallet_transfers = WalletTransfersResource(self._http)
        return self._wallet_transfers

    def wallet_transactions(self) -> WalletTransactionsResource:
        if self._wallet_transactions is None:
            self._wallet_transactions = WalletTransactionsResource(self._http)
        return self._wallet_transactions

    def virtual_accounts(self) -> VirtualAccountsResource:
        if self._virtual_accounts is None:
            self._virtual_accounts = VirtualAccountsResource(self._http)
        return self._virtual_accounts

    def cards(self) -> CardsResource:
        if self._cards is None:
            self._cards = CardsResource(self._http)
        return self._cards

    def card_programs(self) -> CardProgramsResource:
        if self._card_programs is None:
            self._card_programs = CardProgramsResource(self._http)
        return self._card_programs

    def identities(self) -> IdentitiesResource:
        if self._identities is None:
            self._identities = IdentitiesResource(self._http)
        return self._identities

    def verification(self) -> VerificationResource:
        if self._verification is None:
            self._verification = VerificationResource(self._http)
        return self._verification

    def fraud(self) -> FraudResource:
        if self._fraud is None:
            self._fraud = FraudResource(self._http)
        return self._fraud

    def data(self) -> DataResource:
        if self._data is None:
            self._data = DataResource(self._http)
        return self._data

    # --- Lifecycle ---

    async def aclose(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.aclose()

    async def __aenter__(self) -> RapydClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()
