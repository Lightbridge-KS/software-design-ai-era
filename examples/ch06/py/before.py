"""Chapter 6 · BEFORE: a cart that cannot protect itself.

Everything is public, so nothing is safe. `total` is a plain attribute the
caller must remember to recompute (they won't), and `discount_rate` accepts
any number at all. The object has no way to keep its own promises.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LineItem:
    name: str
    price: float


@dataclass
class ShoppingCart:
    items: list[LineItem] = field(default_factory=list)
    discount_rate: float = 0.0
    total: float = 0.0  # a cached field the caller must keep in sync by hand

    def recompute(self) -> None:
        subtotal = sum(item.price for item in self.items)
        self.total = round(subtotal * (1 - self.discount_rate), 2)
