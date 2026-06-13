"""Chapter 11 · Adapter: make third-party code fit an interface we own.

The SDK we don't own speaks cents and dicts; our codebase speaks dollars and
Receipts. The adapter implements our interface and translates — so Stripe's
shape never leaks past this one class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class Receipt:
    provider: str
    amount: float
    confirmation: str


class IPaymentGateway(ABC):
    """Our target interface (we own it → ABC)."""

    @abstractmethod
    def charge(self, amount: float) -> Receipt: ...


class StripeClient:
    """A third-party SDK we do NOT own — different method, cents, returns a dict."""

    def create_charge(self, amount_cents: int, currency: str = "usd") -> dict:
        return {"id": f"ch_{amount_cents}", "paid": True, "currency": currency}


class StripeGateway(IPaymentGateway):
    """The Adapter: fits our interface, delegates and translates to the adaptee."""

    def __init__(self, client: StripeClient) -> None:
        self._client = client

    def charge(self, amount: float) -> Receipt:
        resp = self._client.create_charge(int(round(amount * 100)))  # dollars → cents
        return Receipt("stripe", amount, resp["id"])                 # dict → Receipt


@runtime_checkable
class SupportsCharge(Protocol):
    """Depend on a shape, not a base class — for code we can't make inherit ours."""

    def charge(self, amount: float) -> Receipt: ...


class InHouseGateway:
    """Inherits nothing of ours, yet already matches SupportsCharge by shape."""

    def charge(self, amount: float) -> Receipt:
        return Receipt("inhouse", amount, f"ih-{int(amount * 100)}")
