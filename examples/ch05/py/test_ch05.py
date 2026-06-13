"""Chapter 5 tests — coupling made executable.

Three claims:
  1. The refactor preserved behavior (before == after).
  2. The caller has Least Knowledge: the after's free_shipping never mentions
     'membership' or 'tier' — so remodeling that graph won't touch it.
  3. Dependency direction: the domain model imports nothing volatile (no I/O).
"""

import pathlib
from types import ModuleType

import pytest

import after
import before

# (tier, subtotal, expected free shipping)
CASES = [
    ("gold", 150.0, True),
    ("gold", 50.0, False),     # VIP, but under the threshold
    ("standard", 150.0, False),
    ("standard", 50.0, False),
]


def make_order(mod: ModuleType, tier: str, price: float) -> object:
    customer = mod.Customer("Sam", "s@x.com", mod.Membership(tier))
    return mod.Order(customer, [mod.LineItem("a", price)])


@pytest.mark.parametrize("tier,price,expected", CASES)
def test_refactor_preserved_behavior(tier: str, price: float, expected: bool) -> None:
    b = before.free_shipping(make_order(before, tier, price))
    a = after.free_shipping(make_order(after, tier, price))
    assert b == a == expected


def test_caller_has_least_knowledge() -> None:
    """The after's free_shipping asks one question; it knows no graph shape."""
    src = pathlib.Path(after.__file__).read_text()
    body = src.split("def free_shipping")[1]
    assert "membership" not in body
    assert "tier" not in body


def test_domain_depends_on_nothing_volatile() -> None:
    """Dependency direction: the stable model imports no I/O (depend inward)."""
    src = pathlib.Path(after.__file__).read_text()
    for volatile in ("smtplib", "import json", "import requests", "pathlib"):
        assert volatile not in src
