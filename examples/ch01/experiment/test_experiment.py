"""The chapter's claims about the experiment, as executable facts.

Three modules, all named discounts.py: the starter and the two verbatim
agent outcomes. The tests pin what Chapter 1 asserts about them — including
the silent error-contract change in outcome A.
"""

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

HERE = Path(__file__).parent


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


starter = load("starter_discounts", HERE / "starter" / "discounts.py")
outcome_a = load("outcome_a_discounts", HERE / "outcome-a" / "discounts.py")
outcome_b = load("outcome_b_discounts", HERE / "outcome-b" / "discounts.py")

MODULES = {"starter": starter, "outcome_a": outcome_a, "outcome_b": outcome_b}
KINDS = ["none", "ten_percent", "coupon5", "member"]


def make_order(mod: ModuleType, is_member: bool) -> object:
    items = [mod.LineItem("coffee", 12.50), mod.LineItem("mug", 7.50)]
    return mod.Order(items=items, is_member=is_member)


@pytest.mark.parametrize("kind", KINDS)
@pytest.mark.parametrize("is_member", [False, True])
def test_all_three_versions_compute_identical_totals(kind: str, is_member: bool) -> None:
    totals = {
        name: mod.apply_discount(make_order(mod, is_member), kind)
        for name, mod in MODULES.items()
    }
    assert totals["outcome_a"] == totals["starter"]
    assert totals["outcome_b"] == totals["starter"]


def error_message(mod: ModuleType) -> str:
    with pytest.raises(ValueError) as exc_info:
        mod.apply_discount(make_order(mod, False), "bogus")
    return str(exc_info.value)


def test_outcome_b_preserves_the_error_contract() -> None:
    assert error_message(outcome_b) == error_message(starter)


def test_outcome_a_silently_changed_the_error_contract() -> None:
    """The chapter's key exhibit: helpful, unrequested, and breaking."""
    assert error_message(starter) == "unknown discount: bogus"
    assert error_message(outcome_a) != error_message(starter)
    assert "expected one of" in error_message(outcome_a)
