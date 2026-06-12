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


DiscountFn = Callable[[Order], float]


def apply_discount(order: Order, kind: str) -> float:
    """Return the order total after the given discount."""
    discount = _DISCOUNTS.get(kind)
    if discount is None:
        known = ", ".join(sorted(_DISCOUNTS))
        raise ValueError(f"unknown discount: {kind!r} (expected one of: {known})")
    return discount(order)


def _no_discount(order: Order) -> float:
    return order.subtotal


def _ten_percent(order: Order) -> float:
    return order.subtotal * 0.90


def _coupon_5_off(order: Order) -> float:
    return max(order.subtotal - 5.00, 0.0)


def _member(order: Order) -> float:
    return order.subtotal * 0.85 if order.is_member else order.subtotal


# To add a discount: define a DiscountFn above and register it here.
_DISCOUNTS: dict[str, DiscountFn] = {
    "none": _no_discount,
    "ten_percent": _ten_percent,
    "coupon5": _coupon_5_off,
    "member": _member,
}
