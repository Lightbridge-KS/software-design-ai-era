"""Chapter 14 · State: the order lifecycle as states that own their transitions.

Each state is a class that knows which transitions are legal. Illegal moves
(shipping an unpaid order) raise instead of silently corrupting a status string.
"""

from __future__ import annotations


class IllegalTransition(Exception):
    """Raised when a transition is not allowed from the current state."""


class OrderState:
    """Base state: every transition is illegal by default; states allow some."""

    name: str = "base"

    def pay(self, order: Order) -> None:
        raise IllegalTransition(f"cannot pay from {self.name}")

    def ship(self, order: Order) -> None:
        raise IllegalTransition(f"cannot ship from {self.name}")

    def cancel(self, order: Order) -> None:
        raise IllegalTransition(f"cannot cancel from {self.name}")


class Cart(OrderState):
    name = "cart"

    def pay(self, order: Order) -> None:
        order.state = Paid()

    def cancel(self, order: Order) -> None:
        order.state = Cancelled()


class Paid(OrderState):
    name = "paid"

    def ship(self, order: Order) -> None:
        order.state = Shipped()

    def cancel(self, order: Order) -> None:
        order.state = Cancelled()


class Shipped(OrderState):
    name = "shipped"  # terminal: no transition overridden, so all raise


class Cancelled(OrderState):
    name = "cancelled"  # terminal


class Order:
    """The context: delegates each action to its current state object."""

    def __init__(self) -> None:
        self.state: OrderState = Cart()

    def pay(self) -> None:
        self.state.pay(self)

    def ship(self) -> None:
        self.state.ship(self)

    def cancel(self) -> None:
        self.state.cancel(self)

    @property
    def status(self) -> str:
        return self.state.name
