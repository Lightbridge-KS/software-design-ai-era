"""Chapter 8 · AFTER: open for extension via an injected interface.

process_payment depends on the IPaymentGateway abstraction, not on concrete
providers. Adding a provider is a new class; the core is never edited.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class Receipt:
    provider: str
    amount: float
    confirmation: str


class IPaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> Receipt:
        """Charge ``amount``. Postcondition: returns a Receipt for that amount."""


class CardGateway(IPaymentGateway):
    def charge(self, amount: float) -> Receipt:
        return Receipt("card", amount, f"card-{int(amount * 100)}")


class PayPalGateway(IPaymentGateway):
    def charge(self, amount: float) -> Receipt:
        return Receipt("paypal", amount, f"pp-{int(amount * 100)}")


def process_payment(gateway: IPaymentGateway, amount: float) -> Receipt:
    """Open for extension: a new gateway is a new class, not an edit here."""
    return gateway.charge(amount)


class BadGateway(IPaymentGateway):
    """A Liskov violation: substitutable in name only — breaks the contract."""

    def charge(self, amount: float) -> Receipt:  # type: ignore[return]
        return None  # type: ignore[return-value]  # violates the postcondition


@runtime_checkable
class SupportsCharge(Protocol):
    """Structural interface for code we don't own — matches by shape, not name."""

    def charge(self, amount: float) -> Receipt: ...


class ThirdPartyWallet:
    """A third-party gateway that does NOT inherit IPaymentGateway."""

    def charge(self, amount: float) -> Receipt:
        return Receipt("wallet", amount, f"w-{int(amount * 100)}")
