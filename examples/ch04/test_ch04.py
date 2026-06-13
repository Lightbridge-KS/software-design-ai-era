"""Chapter 4 tests — the split preserves behavior, and unlocks isolation.

Two claims:
  1. Splitting by responsibility changed no observable behavior (before == after).
  2. The cohesion payoff: pricing is now testable with NO email server and NO
     filesystem, because it no longer depends on them.
"""

from pathlib import Path

import pytest

import before
import checkout as after
import persistence
import pricing
from models import Customer, LineItem, Order

CASES = [
    Order(Customer("Sam", "s@x.com"), [LineItem("a", 100.0)], country="US"),
    Order(Customer("Mia", "m@x.com", is_member=True), [LineItem("a", 100.0)], country="US"),
    Order(Customer("Lena", "l@x.com"), [LineItem("a", 80.0)], country="DE", gift_wrap=True),
    Order(Customer("Ken", "k@x.com", is_member=True), [LineItem("a", 50.0)], country="JP"),
    Order(Customer("Ana", "a@x.com"), [LineItem("a", 30.0)], country="CA"),  # no tax
]


@pytest.fixture(autouse=True)
def isolate_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(before, "ORDERS_FILE", tmp_path / "before.json")
    monkeypatch.setattr(persistence, "ORDERS_FILE", tmp_path / "after.json")


@pytest.mark.parametrize("order", CASES)
def test_split_preserves_behavior(order: Order) -> None:
    assert after.checkout(order, "tok", send_email=False) == before.checkout(
        order, "tok", send_email=False
    )


@pytest.mark.parametrize("order", CASES)
def test_pricing_is_pure_no_io_needed(order: Order) -> None:
    """The cohesion payoff: this assertion touches no SMTP and no disk."""
    total = pricing.order_total(order)
    assert isinstance(total, float)
    assert total == round(total, 2)


def test_member_pricing_is_discounted_before_tax() -> None:
    member = Order(Customer("Mia", "m@x.com", is_member=True), [LineItem("a", 100.0)])
    # 100 * 0.85 = 85; +7% = 90.95; +5.00 = 95.95 — verifiable without any I/O
    assert pricing.order_total(member) == 95.95
