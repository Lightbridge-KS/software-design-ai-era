"""Chapter 7 tests — contracts made executable.

The before tests demonstrate the surprises an uncontracted function allows.
The after tests prove the promise is kept: bad input fails fast at the
boundary, and an invalid Percent cannot be constructed at all.
"""

import pytest

import after
import before
from after import Percent


# --- BEFORE: the function astonishes ----------------------------------------

def test_before_silent_unit_confusion() -> None:
    # caller meant 20% but passed 0.2 (a fraction): a 0.2% discount, no warning
    assert before.apply_discount(100.0, 0.2) == 99.8


def test_before_allows_negative_price() -> None:
    # 150% off -> a negative price, returned without complaint
    assert before.apply_discount(100.0, 150.0) == -50.0


# --- AFTER: the contract is kept --------------------------------------------

def test_after_correct_discount() -> None:
    assert after.apply_percentage_discount(100.0, 20.0) == 80.0


@pytest.mark.parametrize("bad", [150.0, -5.0])
def test_after_fails_fast_at_boundary(bad: float) -> None:
    with pytest.raises(ValueError):
        after.apply_percentage_discount(100.0, bad)


def test_after_error_names_its_cause() -> None:
    # the failure points at the discount, not at some distant module
    with pytest.raises(ValueError, match="percent"):
        after.apply_percentage_discount(100.0, 150.0)


@pytest.mark.parametrize(
    "price,percent,expected",
    [(100.0, 20.0, 80.0), (10.0, 0.0, 10.0), (10.0, 100.0, 0.0)],
)
def test_after_postcondition_holds(price: float, percent: float, expected: float) -> None:
    result = after.apply_percentage_discount(price, percent)
    assert result == expected
    assert result >= 0.0
    assert result == round(result, 2)


# --- PARSE, DON'T VALIDATE: an invalid Percent cannot exist -----------------

@pytest.mark.parametrize("bad", [150.0, -1.0])
def test_invalid_percent_cannot_be_constructed(bad: float) -> None:
    with pytest.raises(ValueError):
        Percent(bad)


def test_downstream_trusts_the_parsed_type() -> None:
    # discount() does no validation; it relies on Percent having been parsed
    assert after.discount(100.0, Percent(20.0)) == 80.0
