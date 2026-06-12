"""Discount handling for checkout-lite."""

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


def apply_discount(order: Order, kind: str) -> float:
    """Return the order total after the given discount."""
    if kind == "none":
        return order.subtotal
    elif kind == "ten_percent":
        return order.subtotal * 0.90
    elif kind == "coupon5":
        return max(order.subtotal - 5.00, 0.0)
    elif kind == "member":
        if order.is_member:
            return order.subtotal * 0.85
        return order.subtotal
    else:
        raise ValueError(f"unknown discount: {kind}")
