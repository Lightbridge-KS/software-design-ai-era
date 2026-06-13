"""Chapter 5 · BEFORE: a train wreck and ask-then-decide, in one line.

free_shipping reaches through customer -> membership -> tier (content
coupling: it now depends on the shape of three classes), then pulls the
order's subtotal out to make a decision the order could make itself.
"""

from dataclasses import dataclass, field

FREE_SHIPPING_MIN = 100.0


@dataclass(frozen=True)
class Membership:
    tier: str  # "standard" | "gold"


@dataclass(frozen=True)
class Customer:
    name: str
    email: str
    membership: Membership


@dataclass(frozen=True)
class LineItem:
    name: str
    price: float


@dataclass(frozen=True)
class Order:
    customer: Customer
    items: list[LineItem] = field(default_factory=list)
    country: str = "US"
    gift_wrap: bool = False

    @property
    def subtotal(self) -> float:
        return sum(item.price for item in self.items)


def free_shipping(order: Order) -> bool:
    # talks to strangers (customer.membership.tier) and asks-then-decides
    return order.customer.membership.tier == "gold" and order.subtotal >= FREE_SHIPPING_MIN
