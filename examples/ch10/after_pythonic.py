"""Chapter 10 · AFTER, Pythonic form.

A strategy is usually just a function. The RULES dict is the registry —
the single place where "which rules exist" is recorded.
"""

from collections.abc import Callable

from models import Order

DiscountRule = Callable[[Order], float]


def no_discount(order: Order) -> float:
    return order.subtotal


def percentage_off(rate: float) -> DiscountRule:
    """A closure carries configuration the way an __init__ would, without a class."""
    def rule(order: Order) -> float:
        return order.subtotal * (1 - rate)
    return rule


def coupon_off(amount: float) -> DiscountRule:
    def rule(order: Order) -> float:
        return max(order.subtotal - amount, 0.0)
    return rule


def member_discount(order: Order) -> float:
    return order.subtotal * 0.85 if order.is_member else order.subtotal


RULES: dict[str, DiscountRule] = {
    "none": no_discount,
    "ten_percent": percentage_off(0.10),
    "coupon5": coupon_off(5.00),
    "member": member_discount,
}


def apply_discount(order: Order, rule: DiscountRule) -> float:
    return rule(order)
