"""Chapter 5 · AFTER: ask one object one question.

Each object answers for what it owns, talking only to immediate friends.
The caller knows nothing about membership or tiers — so when that graph is
remodeled, the caller doesn't move.
"""

from dataclasses import dataclass, field

FREE_SHIPPING_MIN = 100.0


@dataclass(frozen=True)
class Membership:
    tier: str  # "standard" | "gold"

    def is_gold(self) -> bool:
        return self.tier == "gold"


@dataclass(frozen=True)
class Customer:
    name: str
    email: str
    membership: Membership

    def is_vip(self) -> bool:
        return self.membership.is_gold()  # one hop, to an immediate friend


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

    def qualifies_for_free_shipping(self) -> bool:
        return self.customer.is_vip() and self.subtotal >= FREE_SHIPPING_MIN


def free_shipping(order: Order) -> bool:
    return order.qualifies_for_free_shipping()  # knows nothing of the customer graph
