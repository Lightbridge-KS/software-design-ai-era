"""checkout-lite pricing — the existing, clean rate logic."""

from models import Order, PricingBreakdown

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


def price_order(order: Order) -> PricingBreakdown:
    """Return an itemized breakdown of all charges for an order."""
    subtotal = round(order.subtotal, 2)
    raw_discounted = member_discount(subtotal, order.customer.is_member)
    discounted = round(raw_discounted, 2)
    tax = round(tax_for(raw_discounted, order.country), 2)
    shipping = round(shipping_for(order.country, order.gift_wrap), 2)
    total = round(discounted + tax + shipping, 2)
    return PricingBreakdown(
        subtotal=subtotal,
        member_discount=round(subtotal - discounted, 2),
        discounted=discounted,
        tax=tax,
        shipping=shipping,
        total=total,
    )


def order_total(order: Order) -> float:
    """Return the final total: discounted subtotal + tax + shipping."""
    return price_order(order).total
