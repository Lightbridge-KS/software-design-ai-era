"""Chapter 15 · Visitor: add operations over a node tree without editing nodes.

The line-item tree from Chapter 12 (Product leaf, Bundle composite). A visitor
carries one operation across every node type via double dispatch — a new
operation is a new visitor, and the node classes never change. The Pythonic
replacement, total_via_match, does the same with structural pattern matching.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


class LineItemVisitor(ABC, Generic[T]):
    @abstractmethod
    def visit_product(self, product: Product) -> T: ...

    @abstractmethod
    def visit_bundle(self, bundle: Bundle) -> T: ...


class LineItem(ABC):
    @abstractmethod
    def accept(self, visitor: LineItemVisitor[T]) -> T: ...


@dataclass
class Product(LineItem):
    name: str
    price: float

    def accept(self, visitor: LineItemVisitor[T]) -> T:
        return visitor.visit_product(self)  # dispatch to the product branch


@dataclass
class Bundle(LineItem):
    name: str
    items: list[LineItem] = field(default_factory=list)

    def accept(self, visitor: LineItemVisitor[T]) -> T:
        return visitor.visit_bundle(self)  # dispatch to the bundle branch


class TotalPriceVisitor(LineItemVisitor[float]):
    def visit_product(self, product: Product) -> float:
        return product.price

    def visit_bundle(self, bundle: Bundle) -> float:
        return sum(item.accept(self) for item in bundle.items)


class CountItemsVisitor(LineItemVisitor[int]):
    def visit_product(self, product: Product) -> int:
        return 1

    def visit_bundle(self, bundle: Bundle) -> int:
        return sum(item.accept(self) for item in bundle.items)


def total_via_match(item: LineItem) -> float:
    """The Pythonic replacement: structural match instead of double dispatch."""
    match item:
        case Product(price=price):
            return price
        case Bundle(items=items):
            return sum(total_via_match(child) for child in items)
    raise TypeError(f"unknown line item: {item!r}")
