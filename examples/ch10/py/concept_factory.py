"""Factory — canonical conceptual example (runnable).

The classical Factory Method shape: a Creator declares a factory method that
returns a Product; subclasses decide the concrete Product. Read this as the
structure the *name* denotes — then see the Pythonic registry form below, which
is what you will usually write.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable


# --- Canonical: Factory Method (a hierarchy decides its product) -------------

class Product(ABC):
    @abstractmethod
    def operation(self) -> str: ...


class ConcreteProductA(Product):
    def operation(self) -> str:
        return "result-A"


class ConcreteProductB(Product):
    def operation(self) -> str:
        return "result-B"


class Creator(ABC):
    @abstractmethod
    def factory_method(self) -> Product:
        """Subclasses choose the concrete Product; the base stays independent."""

    def operation(self) -> str:
        product = self.factory_method()   # uses the product without naming its type
        return f"Creator works with {product.operation()}"


class CreatorA(Creator):
    def factory_method(self) -> Product:
        return ConcreteProductA()


class CreatorB(Creator):
    def factory_method(self) -> Product:
        return ConcreteProductB()


# --- Pythonic: a registry of constructors IS the factory --------------------

_PRODUCTS: dict[str, Callable[[], Product]] = {
    "a": ConcreteProductA,
    "b": ConcreteProductB,
}


def make_product(kind: str) -> Product:
    try:
        return _PRODUCTS[kind]()        # a class is already a callable
    except KeyError:
        raise ValueError(f"unknown product: {kind}") from None


if __name__ == "__main__":
    print(CreatorA().operation())        # Creator works with result-A
    print(make_product("b").operation()) # result-B
