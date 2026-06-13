"""Chapter 12 · Composite: treat a tree of line items uniformly.

A Product is a leaf; a Bundle is a composite that holds other line items —
products or sub-bundles. Both answer price(), so a cart totals itself with no
isinstance checks and no special-casing of branches versus leaves.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class LineItem(ABC):
    """The component interface — shared by leaf and composite alike."""

    @abstractmethod
    def price(self) -> float: ...


class Product(LineItem):
    """A leaf: a single sellable item."""

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self._price = price

    def price(self) -> float:
        return self._price


class Bundle(LineItem):
    """A composite: a sellable thing made of other line items."""

    def __init__(self, name: str, items: list[LineItem] | None = None) -> None:
        self.name = name
        self._items: list[LineItem] = list(items) if items else []

    def add(self, item: LineItem) -> None:
        self._items.append(item)

    def price(self) -> float:
        return sum(item.price() for item in self._items)  # recurse, uniformly


def cart_total(items: list[LineItem]) -> float:
    """The client treats leaf and branch identically — no type checks."""
    return sum(item.price() for item in items)
