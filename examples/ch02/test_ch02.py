"""Chapter 2 tests — the tangle WORKS.

The chapter's central distinction: this code is badly designed, not broken.
These tests pass. Good tests on tangled code is exactly the trap — green
checkmarks say nothing about whether the next change will be safe.
"""

from pathlib import Path

import pytest

import checkout_tangle
from models import Customer, LineItem, Order


@pytest.fixture(autouse=True)
def isolate_orders_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(checkout_tangle, "ORDERS_FILE", tmp_path / "orders.json")


def make_order(
    customer: Customer | None = None,
    items: list[LineItem] | None = None,
    country: str = "US",
    gift_wrap: bool = False,
) -> Order:
    return Order(
        customer=customer or Customer("Sam", "sam@example.com"),
        items=items if items is not None else [LineItem("coffee", 100.00)],
        country=country,
        gift_wrap=gift_wrap,
    )


def test_us_nonmember_total() -> None:
    # 100 + 7% tax + 5.00 shipping
    assert checkout_tangle.checkout(make_order(), "tok", send_email=False) == 112.00


def test_member_discount_applies_before_tax() -> None:
    member = Customer("Mia", "mia@example.com", is_member=True)
    # 100 * 0.85 = 85; +7% = 90.95; +5.00 shipping = 95.95
    total = checkout_tangle.checkout(make_order(customer=member), "tok", send_email=False)
    assert total == 95.95


def test_gift_wrap_adds_fee() -> None:
    plain = checkout_tangle.checkout(make_order(), "tok", send_email=False)
    wrapped = checkout_tangle.checkout(make_order(gift_wrap=True), "tok", send_email=False)
    assert round(wrapped - plain, 2) == 3.50


def test_order_is_persisted() -> None:
    checkout_tangle.checkout(make_order(), "tok", send_email=False)
    assert checkout_tangle.ORDERS_FILE.exists()
    assert "Sam" in checkout_tangle.ORDERS_FILE.read_text()


def test_member_email_failure_never_blocks_the_sale() -> None:
    """No SMTP server in tests; the swallowed OSError must not break checkout."""
    member = Customer("Mia", "mia@example.com", is_member=True)
    total = checkout_tangle.checkout(make_order(customer=member), "tok", send_email=True)
    assert total == 95.95  # sale completes regardless of email
