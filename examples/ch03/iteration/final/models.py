"""checkout-lite domain model."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LineItem:
    name: str
    price: float


@dataclass(frozen=True)
class Customer:
    name: str
    email: str
    is_member: bool = False


@dataclass(frozen=True)
class Order:
    customer: Customer
    items: list[LineItem] = field(default_factory=list)
    country: str = "US"
    gift_wrap: bool = False

    @property
    def subtotal(self) -> float:
        return sum(item.price for item in self.items)


@dataclass(frozen=True)
class PricingBreakdown:
    subtotal: float
    member_discount: float
    discounted: float
    tax: float
    shipping: float
    total: float
