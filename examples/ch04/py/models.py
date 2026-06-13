"""checkout-lite domain model (shared by before and after)."""

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
