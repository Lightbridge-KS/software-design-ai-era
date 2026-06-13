"""Chapter 6 · AFTER: a cart that keeps its own promises.

A narrow public surface over a hidden implementation. `total` is computed, so
it can never go stale or lie; `discount_rate` is validated; the item list is
hidden behind a read-only view. There is no way to put this cart in an illegal
state from the outside.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LineItem:
    name: str
    price: float


class ShoppingCart:
    def __init__(self) -> None:
        self._items: list[LineItem] = []
        self._discount_rate: float = 0.0

    def add_item(self, item: LineItem) -> None:
        self._items.append(item)

    @property
    def items(self) -> tuple[LineItem, ...]:
        return tuple(self._items)  # a read-only view; mutating it can't corrupt us

    @property
    def discount_rate(self) -> float:
        return self._discount_rate

    @discount_rate.setter
    def discount_rate(self, rate: float) -> None:
        if not 0.0 <= rate <= 1.0:
            raise ValueError(f"discount_rate must be in [0, 1], got {rate}")
        self._discount_rate = rate

    @property
    def total(self) -> float:
        subtotal = sum(item.price for item in self._items)
        return round(subtotal * (1 - self._discount_rate), 2)
