"""Shared checkout-lite model for Chapter 9 examples.

Real money arithmetic wants Decimal or integer cents; float keeps these
teaching examples short.
"""

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
