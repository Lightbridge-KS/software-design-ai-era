"""checkout-lite pricing — the existing, clean rate logic."""

from models import Order

TAX_RATES = {"US": 0.07, "DE": 0.19, "JP": 0.10}
EU_COUNTRIES = ("DE", "FR", "NL")


def member_discount(subtotal: float, is_member: bool) -> float:
    """Return the subtotal after the member discount."""
    return subtotal * 0.85 if is_member else subtotal


def tax_for(amount: float, country: str) -> float:
    """Return the tax owed on an amount for a country."""
    return amount * TAX_RATES.get(country, 0.0)


def shipping_for(country: str, gift_wrap: bool) -> float:
    """Return the shipping cost for a country, plus gift-wrap if requested."""
    if country == "US":
        base = 5.00
    elif country in EU_COUNTRIES:
        base = 9.90
    else:
        base = 24.90
    return base + (3.50 if gift_wrap else 0.0)


def order_total(order: Order) -> float:
    """Return the final total: discounted subtotal + tax + shipping."""
    discounted = member_discount(order.subtotal, order.customer.is_member)
    tax = tax_for(discounted, order.country)
    shipping = shipping_for(order.country, order.gift_wrap)
    return round(discounted + tax + shipping, 2)
