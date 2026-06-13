"""Shared checkout-lite model for Chapter 2.

Real money arithmetic wants Decimal or integer cents; float keeps these
teaching examples short.
"""

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
