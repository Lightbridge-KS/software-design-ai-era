"""Chapter 6 tests — encapsulation made executable.

The before tests demonstrate the leaks the open object allows. The after
tests prove the same illegal states are now impossible to reach.
"""

import pytest

import after
import before


# --- BEFORE: the object cannot protect itself -------------------------------

def test_before_total_goes_stale() -> None:
    cart = before.ShoppingCart()
    cart.items.append(before.LineItem("coffee", 12.50))
    # forgot to recompute(): total still claims 0.00
    assert cart.total == 0.0


def test_before_accepts_nonsense_discount() -> None:
    cart = before.ShoppingCart(items=[before.LineItem("coffee", 10.0)])
    cart.discount_rate = 2.0  # 200% off — accepted without complaint
    cart.recompute()
    assert cart.total == -10.0  # a negative price, happily computed


# --- AFTER: the same illegal states are unreachable -------------------------

def test_after_total_is_always_correct() -> None:
    cart = after.ShoppingCart()
    cart.add_item(after.LineItem("coffee", 12.50))
    assert cart.total == 12.50  # computed on read; cannot go stale


def test_after_rejects_invalid_discount() -> None:
    cart = after.ShoppingCart()
    with pytest.raises(ValueError):
        cart.discount_rate = 2.0


def test_after_total_is_read_only() -> None:
    cart = after.ShoppingCart()
    with pytest.raises(AttributeError):
        cart.total = 999.0  # no setter — the lie is unrepresentable


def test_after_items_view_cannot_corrupt_the_cart() -> None:
    cart = after.ShoppingCart()
    cart.add_item(after.LineItem("coffee", 12.50))
    view = cart.items
    assert isinstance(view, tuple)
    with pytest.raises(AttributeError):
        view.append(after.LineItem("sneaky", 0.0))  # tuple has no append
    assert cart.total == 12.50  # internal state untouched


# --- valid usage agrees across both designs ---------------------------------

CASES = [
    ([("coffee", 12.50), ("mug", 7.50)], 0.0),
    ([("beans", 100.0)], 0.10),
    ([], 0.50),
]


@pytest.mark.parametrize("prices,rate", CASES)
def test_valid_usage_matches(prices: list[tuple[str, float]], rate: float) -> None:
    bc = before.ShoppingCart(
        items=[before.LineItem(n, p) for n, p in prices], discount_rate=rate
    )
    bc.recompute()
    ac = after.ShoppingCart()
    for n, p in prices:
        ac.add_item(after.LineItem(n, p))
    ac.discount_rate = rate
    assert bc.total == ac.total
