"""Chapter 14 · Observer: announce order events; subscribers react.

The order flow publishes an event; interested parties subscribe without the
flow knowing who they are. Adding a reaction is one subscribe() call — the core
place_order code never changes.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderPlaced:
    order_id: str
    total: float


Subscriber = Callable[[OrderPlaced], None]


class OrderEvents:
    """The subject: holds subscribers, notifies each on publish."""

    def __init__(self) -> None:
        self._subscribers: list[Subscriber] = []

    def subscribe(self, subscriber: Subscriber) -> None:
        self._subscribers.append(subscriber)

    def publish(self, event: OrderPlaced) -> None:
        for subscriber in self._subscribers:
            subscriber(event)


def place_order(order_id: str, total: float, events: OrderEvents) -> OrderPlaced:
    """The core flow: do the work, then announce — who listens is not its concern."""
    event = OrderPlaced(order_id, total)
    events.publish(event)
    return event
