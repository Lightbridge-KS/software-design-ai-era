"""Chapter 10 · AFTER, classical form.

Strategy as an ABC hierarchy (IDiscountRule) and Template Method for the
receipt skeleton (ReceiptRenderer). This is the form an agent most often
produces when told only "use the Strategy pattern".
"""

from abc import ABC, abstractmethod

from models import Order


# --- Strategy: each discount rule behind a common interface -----------------

class IDiscountRule(ABC):
    @abstractmethod
    def apply(self, order: Order) -> float:
        """Return the order total after this discount."""


class NoDiscount(IDiscountRule):
    def apply(self, order: Order) -> float:
        return order.subtotal


class PercentageOff(IDiscountRule):
    def __init__(self, rate: float) -> None:
        self._rate = rate

    def apply(self, order: Order) -> float:
        return order.subtotal * (1 - self._rate)


class CouponOff(IDiscountRule):
    def __init__(self, amount: float) -> None:
        self._amount = amount

    def apply(self, order: Order) -> float:
        return max(order.subtotal - self._amount, 0.0)


class MemberDiscount(IDiscountRule):
    def apply(self, order: Order) -> float:
        if order.is_member:
            return order.subtotal * 0.85
        return order.subtotal


def apply_discount(order: Order, rule: IDiscountRule) -> float:
    return rule.apply(order)


# --- Template Method: fixed receipt skeleton, varying steps -----------------

class ReceiptRenderer(ABC):
    def render(self, order: Order) -> str:
        """The fixed skeleton. Subclasses supply steps, never the order of steps."""
        return "\n".join(
            [self.header(), self.line_items(order), self.footer(order)]
        )

    @abstractmethod
    def header(self) -> str: ...

    @abstractmethod
    def line_items(self, order: Order) -> str: ...

    def footer(self, order: Order) -> str:
        """Hook: sensible default, override only if the format needs to."""
        return f"Total: {order.subtotal:.2f}"


class PlainTextReceipt(ReceiptRenderer):
    def header(self) -> str:
        return "CHECKOUT-LITE RECEIPT"

    def line_items(self, order: Order) -> str:
        return "\n".join(
            f"{item.name:<20} {item.price:>8.2f}" for item in order.items
        )


class HtmlReceipt(ReceiptRenderer):
    def header(self) -> str:
        return "<h1>Checkout-lite receipt</h1>"

    def line_items(self, order: Order) -> str:
        rows = "".join(
            f"<tr><td>{item.name}</td><td>{item.price:.2f}</td></tr>"
            for item in order.items
        )
        return f"<table>{rows}</table>"

    def footer(self, order: Order) -> str:
        return f"<p>Total: {order.subtotal:.2f}</p>"
