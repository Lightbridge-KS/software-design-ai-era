"""Chapter 11 · Façade: one friendly door over the checkout subsystems.

Placing an order means coordinating four subsystems. The façade hides that
dance behind a single call, so callers depend on one simple thing.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LineItem:
    name: str
    price: float


@dataclass(frozen=True)
class Order:
    items: list[LineItem] = field(default_factory=list)

    @property
    def subtotal(self) -> float:
        return sum(item.price for item in self.items)


@dataclass(frozen=True)
class Receipt:
    total: float
    confirmation: str


# --- the subsystems (each cohesive; see Chapters 4-10) ----------------------

def order_total(order: Order) -> float:
    return round(order.subtotal * 1.07, 2)          # pricing (+7% tax, simplified)


def charge(total: float) -> str:
    return f"ch_{int(total * 100)}"                  # gateway


def send_receipt(order: Order, total: float) -> None:
    """Notification subsystem (I/O elided)."""


def save_order(order: Order, total: float) -> None:
    """Persistence subsystem (I/O elided)."""


# --- the Façade: one call hides the four-step orchestration -----------------

def place_order(order: Order) -> Receipt:
    total = order_total(order)
    confirmation = charge(total)
    send_receipt(order, total)
    save_order(order, total)
    return Receipt(total, confirmation)
