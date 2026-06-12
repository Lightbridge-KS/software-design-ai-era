"""Discount handling for checkout-lite."""

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class LineItem:
    name: str
    price: float


@dataclass(frozen=True)
class Order:
    items: list[LineItem] = field(default_factory=list)
    is_member: bool = False

    @property
    def subtotal(self) -> float:
        return sum(item.price for item in self.items)


def _no_discount(order: Order) -> float:
    return order.subtotal


def _ten_percent(order: Order) -> float:
    return order.subtotal * 0.90


def _coupon5(order: Order) -> float:
    return max(order.subtotal - 5.00, 0.0)


def _member(order: Order) -> float:
    if order.is_member:
        return order.subtotal * 0.85
    return order.subtotal


_DISCOUNT_STRATEGIES: dict[str, Callable[[Order], float]] = {
    "none": _no_discount,
    "ten_percent": _ten_percent,
    "coupon5": _coupon5,
    "member": _member,
}


def apply_discount(order: Order, kind: str) -> float:
    """Return the order total after the given discount."""
    try:
        strategy = _DISCOUNT_STRATEGIES[kind]
    except KeyError:
        raise ValueError(f"unknown discount: {kind}") from None
    return strategy(order)
