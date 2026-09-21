"""
03_abstract_interfaces.py
==========================
Module 2: Object-Oriented Programming & Modular Design
Topic: Abstract Base Classes (ABCs), Formal Contracts, and Dependency Inversion

Concepts Covered:
  - Abstract Base Classes using `abc.ABC` and `@abstractmethod`
  - Defining clean, uncoupled domain contracts/interfaces
  - Adapter implementations:
      * NotificationChannel: EmailNotifier, SMSNotifier, SlackWebhookNotifier
      * PaymentGateway: StripePaymentGateway, PayPalPaymentGateway, MockPaymentGateway
  - Dependency Inversion Principle (DIP): High-level business services (`CheckoutService`)
    depend exclusively on abstractions, not volatile low-level details
  - Swapping implementations dynamically at runtime (e.g. testing vs production)
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict
import uuid


# ─────────────────────────────────────────────────────────────────────────────
# NOTIFICATION CONTRACT & IMPLEMENTATIONS
# ─────────────────────────────────────────────────────────────────────────────

class NotificationChannel(ABC):
    """Abstract interface defining the contract for dispatching notifications."""

    @abstractmethod
    def send(self, recipient: str, subject: str, message: str) -> bool:
        """Send notification to recipient. Return True on success, False otherwise."""
        pass

    @property
    @abstractmethod
    def channel_name(self) -> str:
        """Identifying name of the channel."""
        pass


class EmailNotifier(NotificationChannel):
    """Concrete notifier sending messages via SMTP / Email service."""

    def __init__(self, smtp_server: str = "smtp.mailprovider.com") -> None:
        self._smtp_server = smtp_server

    @property
    def channel_name(self) -> str:
        return "Email (SMTP)"

    def send(self, recipient: str, subject: str, message: str) -> bool:
        print(f"  [EMAIL DISPATCH] Server: {self._smtp_server}")
        print(f"    To     : {recipient}")
        print(f"    Subject: {subject}")
        print(f"    Body   : {message}")
        return True


class SMSNotifier(NotificationChannel):
    """Concrete notifier sending text messages via Telecom gateway."""

    def __init__(self, sender_number: str = "+1-800-555-0199") -> None:
        self._sender_number = sender_number

    @property
    def channel_name(self) -> str:
        return "SMS (Twilio/Telecom)"

    def send(self, recipient: str, subject: str, message: str) -> bool:
        print(f"  [SMS DISPATCH] From: {self._sender_number} -> To: {recipient}")
        print(f"    Text: [{subject}] {message}")
        return True


class SlackWebhookNotifier(NotificationChannel):
    """Concrete notifier posting formatted alerts to a Slack channel."""

    def __init__(self, channel: str = "#finance-alerts") -> None:
        self._channel = channel

    @property
    def channel_name(self) -> str:
        return f"Slack Webhook ({self._channel})"

    def send(self, recipient: str, subject: str, message: str) -> bool:
        print(f"  [SLACK DISPATCH] Channel: {self._channel} (mentioning @{recipient})")
        print(f"    * {subject} * -> {message}")
        return True


# ─────────────────────────────────────────────────────────────────────────────
# PAYMENT GATEWAY CONTRACT & IMPLEMENTATIONS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class PaymentResult:
    success: bool
    transaction_id: str
    amount: float
    currency: str
    gateway_name: str
    error_message: Optional[str] = None


@dataclass
class RefundResult:
    success: bool
    refund_id: str
    original_tx_id: str
    amount: float
    error_message: Optional[str] = None


class PaymentGateway(ABC):
    """Abstract interface defining the contract for processing financial charges and refunds."""

    @abstractmethod
    def charge(self, amount: float, currency: str, customer_token: str) -> PaymentResult:
        """Authorize and settle a charge."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> RefundResult:
        """Process a full or partial refund against an existing charge."""
        pass

    @property
    @abstractmethod
    def gateway_name(self) -> str:
        """Name of the payment processor."""
        pass


class StripePaymentGateway(PaymentGateway):
    """Stripe API adapter implementing the PaymentGateway contract."""

    def __init__(self, api_key: str = "sk_live_stripe_sample_key") -> None:
        self._api_key = api_key
        self._fee_rate = 0.029  # 2.9% + 30c

    @property
    def gateway_name(self) -> str:
        return "Stripe Cloud Gateway"

    def charge(self, amount: float, currency: str, customer_token: str) -> PaymentResult:
        if amount <= 0:
            return PaymentResult(
                success=False, transaction_id="", amount=amount,
                currency=currency, gateway_name=self.gateway_name,
                error_message="Charge amount must be greater than zero."
            )
        if not customer_token.startswith("tok_"):
            return PaymentResult(
                success=False, transaction_id="", amount=amount,
                currency=currency, gateway_name=self.gateway_name,
                error_message=f"Invalid Stripe payment method token: {customer_token!r}."
            )

        tx_id = f"ch_stripe_{uuid.uuid4().hex[:12]}"
        print(f"  [STRIPE API] Settled ${amount:.2f} {currency.upper()} using token {customer_token}. TX: {tx_id}")
        return PaymentResult(
            success=True, transaction_id=tx_id, amount=amount,
            currency=currency, gateway_name=self.gateway_name
        )

    def refund(self, transaction_id: str, amount: float) -> RefundResult:
        ref_id = f"re_stripe_{uuid.uuid4().hex[:12]}"
        print(f"  [STRIPE API] Refunded ${amount:.2f} for charge {transaction_id}. Refund ID: {ref_id}")
        return RefundResult(success=True, refund_id=ref_id, original_tx_id=transaction_id, amount=amount)


class PayPalPaymentGateway(PaymentGateway):
    """PayPal REST API adapter implementing the PaymentGateway contract."""

    def __init__(self, client_id: str = "paypal_client_id_live") -> None:
        self._client_id = client_id

    @property
    def gateway_name(self) -> str:
        return "PayPal Wallet Direct"

    def charge(self, amount: float, currency: str, customer_token: str) -> PaymentResult:
        # PayPal tokens are formatted as email or payer_id
        if "@" not in customer_token and not customer_token.startswith("PAYER_"):
            return PaymentResult(
                success=False, transaction_id="", amount=amount,
                currency=currency, gateway_name=self.gateway_name,
                error_message=f"Invalid PayPal payer identifier: {customer_token!r}."
            )

        tx_id = f"PAYID-{uuid.uuid4().hex[:10].upper()}"
        print(f"  [PAYPAL API] Captured payment ${amount:.2f} {currency} from Payer {customer_token}. TX: {tx_id}")
        return PaymentResult(
            success=True, transaction_id=tx_id, amount=amount,
            currency=currency, gateway_name=self.gateway_name
        )

    def refund(self, transaction_id: str, amount: float) -> RefundResult:
        ref_id = f"REF-{uuid.uuid4().hex[:10].upper()}"
        print(f"  [PAYPAL API] Dispatched PayPal refund ${amount:.2f} for {transaction_id}")
        return RefundResult(success=True, refund_id=ref_id, original_tx_id=transaction_id, amount=amount)


class MockPaymentGateway(PaymentGateway):
    """In-memory test double for unit testing and offline development."""

    def __init__(self, should_succeed: bool = True) -> None:
        self.should_succeed = should_succeed
        self.processed_charges: List[Dict] = []
        self.processed_refunds: List[Dict] = []

    @property
    def gateway_name(self) -> str:
        return "Mock Test Double Gateway"

    def charge(self, amount: float, currency: str, customer_token: str) -> PaymentResult:
        if not self.should_succeed:
            return PaymentResult(
                success=False, transaction_id="", amount=amount,
                currency=currency, gateway_name=self.gateway_name,
                error_message="Simulated mock gateway decline (insufficient test balance)."
            )

        tx_id = f"mock_tx_{len(self.processed_charges) + 1:04d}"
        self.processed_charges.append({
            "tx_id": tx_id, "amount": amount, "currency": currency, "token": customer_token
        })
        return PaymentResult(
            success=True, transaction_id=tx_id, amount=amount,
            currency=currency, gateway_name=self.gateway_name
        )

    def refund(self, transaction_id: str, amount: float) -> RefundResult:
        ref_id = f"mock_ref_{len(self.processed_refunds) + 1:04d}"
        self.processed_refunds.append({"refund_id": ref_id, "tx_id": transaction_id, "amount": amount})
        return RefundResult(success=True, refund_id=ref_id, original_tx_id=transaction_id, amount=amount)


# ─────────────────────────────────────────────────────────────────────────────
# HIGH-LEVEL APPLICATION SERVICE (DEPENDENCY INVERSION PRINCIPLE)
# ─────────────────────────────────────────────────────────────────────────────

class OrderCheckoutService:
    """Core domain service orchestrating customer checkouts.

    Notice: This service knows NOTHING about Stripe, PayPal, SMTP, Twilio, or Slack!
    It depends exclusively on the abstract interfaces `PaymentGateway` and `NotificationChannel`.
    """

    def __init__(
        self,
        payment_gateway: PaymentGateway,
        notification_channel: NotificationChannel,
    ) -> None:
        # Injected abstractions
        self._payment_gateway: PaymentGateway = payment_gateway
        self._notifier: NotificationChannel = notification_channel

    def process_order(
        self,
        order_id: str,
        customer_email: str,
        amount: float,
        currency: str,
        payment_token: str,
    ) -> bool:
        """Process payment and notify customer upon outcome."""
        print(f"\n--- Initiating Checkout for Order: {order_id} (${amount:.2f} {currency}) ---")
        print(f"    Gateway Configured : {self._payment_gateway.gateway_name}")
        print(f"    Notifier Configured: {self._notifier.channel_name}")

        result = self._payment_gateway.charge(amount, currency, payment_token)

        if result.success:
            print(f"  Payment Succeeded! TX ID: {result.transaction_id}")
            # Notify customer
            subject = f"Order Confirmation: #{order_id}"
            body = (
                f"Thank you for your purchase of ${amount:.2f} {currency}. "
                f"Your transaction reference is {result.transaction_id}."
            )
            self._notifier.send(customer_email, subject, body)
            return True
        else:
            print(f"  Payment Failed! Reason: {result.error_message}")
            subject = f"Action Required: Payment Failed for Order #{order_id}"
            body = f"We could not process your payment: {result.error_message}. Please update your payment details."
            self._notifier.send(customer_email, subject, body)
            return False


def main():
    print("=" * 70)
    print("  EXERCISE 03: ABSTRACT INTERFACES & DEPENDENCY INVERSION")
    print("=" * 70)

    # 1. Setup Production Scenario A: Stripe + Email Notifier
    print("\n[Scenario 1] Production Flow: Stripe + Email Notifications")
    stripe_gateway = StripePaymentGateway()
    email_notifier = EmailNotifier()
    checkout_service_a = OrderCheckoutService(stripe_gateway, email_notifier)

    success_a = checkout_service_a.process_order(
        order_id="ORD-9001",
        customer_email="alice.client@deltaiot.com",
        amount=149.99,
        currency="USD",
        payment_token="tok_visa_4242",
    )
    print(f"  Order Result: {'COMPLETED' if success_a else 'FAILED'}")

    # 2. Setup Production Scenario B: PayPal + Slack Notifications
    print("\n[Scenario 2] Alternative Gateway: PayPal + Slack Team Webhook")
    paypal_gateway = PayPalPaymentGateway()
    slack_notifier = SlackWebhookNotifier("#sales-realtime")
    checkout_service_b = OrderCheckoutService(paypal_gateway, slack_notifier)

    success_b = checkout_service_b.process_order(
        order_id="ORD-9002",
        customer_email="bob.buyer@deltaiot.com",
        amount=89.50,
        currency="USD",
        payment_token="bob.buyer@deltaiot.com",
    )
    print(f"  Order Result: {'COMPLETED' if success_b else 'FAILED'}")

    # 3. Setup Test Scenario C: Mock Gateway + SMS Notifier (Simulated Failure)
    print("\n[Scenario 3] Unit Testing / Failure Handling: Mock Gateway + SMS")
    mock_failing_gateway = MockPaymentGateway(should_succeed=False)
    sms_notifier = SMSNotifier("+1-555-0100")
    checkout_service_test = OrderCheckoutService(mock_failing_gateway, sms_notifier)

    success_c = checkout_service_test.process_order(
        order_id="ORD-9003",
        customer_email="+1-555-0144",
        amount=500.00,
        currency="USD",
        payment_token="tok_card_declined",
    )
    print(f"  Order Result: {'COMPLETED' if success_c else 'FAILED'}")

    print("\nAbstract interfaces & dependency inversion demonstration complete!\n")


if __name__ == "__main__":
    main()
