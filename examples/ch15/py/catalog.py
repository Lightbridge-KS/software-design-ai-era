"""Chapter 15 · Iterator: traverse without exposing the container.

A Catalog is iterable (`for product in catalog`) without leaking its internal
list. paged() is a generator: it streams fixed-size batches lazily instead of
building them all up front.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    price: float


class Catalog:
    def __init__(self, products: list[Product]) -> None:
        self._products = products

    def __iter__(self) -> Iterator[Product]:
        return iter(self._products)  # delegate to the list's own iterator

    def __len__(self) -> int:
        return len(self._products)


def paged(products: list[Product], size: int) -> Iterator[list[Product]]:
    """Generator: yield fixed-size batches lazily, one at a time."""
    for start in range(0, len(products), size):
        yield products[start : start + size]
