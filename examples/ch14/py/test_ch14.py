"""Chapter 14 tests — Observer and State, made executable.

Observer: every subscriber receives the published event, and no subscribers is
fine. State: the lifecycle walks legal transitions and rejects illegal ones.
"""

import pytest

from events import OrderEvents, OrderPlaced, place_order
from order_state import IllegalTransition, Order


# --- Observer ---------------------------------------------------------------

def test_subscribers_all_receive_the_event() -> None:
    events = OrderEvents()
    seen: list[str] = []
    events.subscribe(lambda e: seen.append(f"receipt:{e.order_id}"))
    events.subscribe(lambda e: seen.append(f"inventory:{e.total}"))
    place_order("A1", 30.0, events)
    assert seen == ["receipt:A1", "inventory:30.0"]


def test_no_subscribers_is_fine() -> None:
    events = OrderEvents()
    event = place_order("A2", 10.0, events)
    assert event == OrderPlaced("A2", 10.0)


# --- State ------------------------------------------------------------------

def test_legal_lifecycle_path() -> None:
    order = Order()
    assert order.status == "cart"
    order.pay()
    assert order.status == "paid"
    order.ship()
    assert order.status == "shipped"


def test_illegal_transition_raises() -> None:
    order = Order()
    with pytest.raises(IllegalTransition):
        order.ship()  # cannot ship from cart


def test_cancel_from_cart_and_from_paid() -> None:
    from_cart = Order()
    from_cart.cancel()
    assert from_cart.status == "cancelled"

    from_paid = Order()
    from_paid.pay()
    from_paid.cancel()
    assert from_paid.status == "cancelled"
