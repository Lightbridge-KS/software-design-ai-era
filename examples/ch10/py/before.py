"""Chapter 10 · BEFORE: construction scattered across call sites.

Chapter 8 made *using* a gateway open-closed by injecting it. But something
still has to *build* the right one — and that if/elif is now copy-pasted
wherever a gateway is needed. A new provider means hunting down every copy.
"""

from abc import ABC, abstractmethod
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


def checkout(method: str, amount: float) -> Receipt:
    if method == "card":
        gateway: IPaymentGateway = CardGateway()
    elif method == "paypal":
        gateway = PayPalGateway()
    else:
        raise ValueError(f"unknown payment method: {method}")
    return gateway.charge(amount)


def refund(method: str, amount: float) -> Receipt:
    if method == "card":                       # the same switch, copied
        gateway: IPaymentGateway = CardGateway()
    elif method == "paypal":
        gateway = PayPalGateway()
    else:
        raise ValueError(f"unknown payment method: {method}")
    return gateway.charge(-amount)
