"""Chapter 12 · Decorator: add behavior to a gateway without editing it.

Each decorator implements IPaymentGateway and wraps ONE gateway, forwarding
charge() while adding a cross-cutting concern. Decorators stack at runtime:
RetryingGateway(LoggingGateway(StripeGateway())).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Receipt:
    provider: str
    amount: float
    confirmation: str


class TransientError(Exception):
    """A failure worth retrying."""


class IPaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> Receipt: ...


class StripeGateway(IPaymentGateway):
    """The real gateway — the concrete component we wrap."""

    def charge(self, amount: float) -> Receipt:
        return Receipt("stripe", amount, f"ch_{int(round(amount * 100))}")


class GatewayDecorator(IPaymentGateway):
    """Base decorator: holds ONE wrapped gateway, forwards by default."""

    def __init__(self, wrapped: IPaymentGateway) -> None:
        self._wrapped = wrapped

    def charge(self, amount: float) -> Receipt:
        return self._wrapped.charge(amount)


class LoggingGateway(GatewayDecorator):
    """Augment: record around the delegated charge."""

    def __init__(self, wrapped: IPaymentGateway, log: list[str]) -> None:
        super().__init__(wrapped)
        self._log = log

    def charge(self, amount: float) -> Receipt:
        self._log.append(f"charging {amount:.2f}")
        receipt = self._wrapped.charge(amount)
        self._log.append(f"charged {receipt.confirmation}")
        return receipt


class RetryingGateway(GatewayDecorator):
    """Augment: retry the delegated charge on a transient failure."""

    def __init__(self, wrapped: IPaymentGateway, retries: int = 2) -> None:
        super().__init__(wrapped)
        self._retries = retries

    def charge(self, amount: float) -> Receipt:
        last: Exception | None = None
        for _ in range(self._retries + 1):
            try:
                return self._wrapped.charge(amount)
            except TransientError as exc:  # transient → try again
                last = exc
        assert last is not None
        raise last  # retries exhausted
