"""Chapter 10 tests — the design's claims, executable.

Note what good design does to the tests: each rule is tested alone, with no
dispatch in the way, and the refactored forms must match the tangle's behavior.
"""

import pytest

import after_classical as classical
import after_pythonic as pythonic
import before
from models import LineItem, Order


@pytest.fixture
def order() -> Order:
    return Order(items=[LineItem("coffee", 12.50), LineItem("mug", 7.50)])


@pytest.fixture
def member_order() -> Order:
    return Order(items=[LineItem("coffee", 20.00)], is_member=True)


# --- Strategy: refactored forms preserve the tangle's behavior --------------

CASES = ["none", "ten_percent", "coupon5", "member"]


@pytest.mark.parametrize("kind", CASES)
def test_classical_matches_before(order: Order, kind: str) -> None:
    rules: dict[str, classical.IDiscountRule] = {
        "none": classical.NoDiscount(),
        "ten_percent": classical.PercentageOff(0.10),
        "coupon5": classical.CouponOff(5.00),
        "member": classical.MemberDiscount(),
    }
    assert classical.apply_discount(order, rules[kind]) == before.apply_discount(order, kind)


@pytest.mark.parametrize("kind", CASES)
def test_pythonic_matches_before(order: Order, kind: str) -> None:
    assert pythonic.apply_discount(order, pythonic.RULES[kind]) == before.apply_discount(order, kind)


# --- Strategy: each rule is testable alone, no dispatch in the way ----------

def test_member_rule_alone(member_order: Order) -> None:
    assert pythonic.member_discount(member_order) == 17.00


def test_member_rule_ignores_non_members(order: Order) -> None:
    assert pythonic.member_discount(order) == order.subtotal


def test_coupon_never_goes_negative() -> None:
    small = Order(items=[LineItem("sticker", 2.00)])
    assert pythonic.coupon_off(5.00)(small) == 0.0


# --- Template Method: skeleton fixed, output identical to the tangle --------

def test_text_receipt_matches_before(order: Order) -> None:
    assert classical.PlainTextReceipt().render(order) == before.render_text_receipt(order)


def test_html_receipt_matches_before(order: Order) -> None:
    assert classical.HtmlReceipt().render(order) == before.render_html_receipt(order)


def test_skeleton_owns_step_order(order: Order) -> None:
    text = classical.PlainTextReceipt().render(order)
    assert text.index("RECEIPT") < text.index("coffee") < text.index("Total:")
