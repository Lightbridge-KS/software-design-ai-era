"""Chapter 10 · AFTER: one factory function, backed by a registry.

A class is already a callable that constructs an instance — so a dict of
classes *is* a factory. Construction knowledge lives in one place; adding a
provider is one registry entry, and every call site just asks make_gateway.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Receipt:
    provider: str
    amount: float


class IPaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> Receipt: ...


class CardGateway(IPaymentGateway):
    def charge(self, amount: float) -> Receipt:
        return Receipt("card", amount)


class PayPalGateway(IPaymentGateway):
    def charge(self, amount: float) -> Receipt:
        return Receipt("paypal", amount)


_GATEWAYS: dict[str, Callable[[], IPaymentGateway]] = {
    "card": CardGateway,
    "paypal": PayPalGateway,
}


def make_gateway(method: str) -> IPaymentGateway:
    """The factory: look up the constructor and call it. Unknown -> fail fast."""
    try:
        return _GATEWAYS[method]()
    except KeyError:
        raise ValueError(f"unknown payment method: {method}") from None


def checkout(method: str, amount: float) -> Receipt:
    return make_gateway(method).charge(amount)


def refund(method: str, amount: float) -> Receipt:
    return make_gateway(method).charge(-amount)
