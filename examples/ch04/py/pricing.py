"""Pricing — answers to one actor: finance/commerce rules.

One reason to change: the money math. No I/O, no email, no disk — which is
exactly why it is testable in isolation.
"""

from models import Order

TAX_RATES = {"US": 0.07, "DE": 0.19, "JP": 0.10}
EU_COUNTRIES = ("DE", "FR", "NL")


def member_discount(subtotal: float, is_member: bool) -> float:
    return subtotal * 0.85 if is_member else subtotal


def tax_for(amount: float, country: str) -> float:
    return amount * TAX_RATES.get(country, 0.0)


def shipping_for(country: str, gift_wrap: bool) -> float:
    if country == "US":
        base = 5.00
    elif country in EU_COUNTRIES:
        base = 9.90
    else:
        base = 24.90
    return base + (3.50 if gift_wrap else 0.0)


def order_total(order: Order) -> float:
    discounted = member_discount(order.subtotal, order.customer.is_member)
    tax = tax_for(discounted, order.country)
    shipping = shipping_for(order.country, order.gift_wrap)
    return round(discounted + tax + shipping, 2)
