"""Chapter 7 · AFTER: the promise written down and enforced.

Two complementary forms:
  - apply_percentage_discount: states its contract, fails fast on bad input
    at the boundary (raise), and asserts its own postcondition internally.
  - Percent + discount: "parse, don't validate" — a raw float becomes a
    proven Percent once, and downstream code trusts it without re-checking.
"""

from dataclasses import dataclass


def apply_percentage_discount(price: float, percent: float) -> float:
    """Return ``price`` reduced by ``percent`` percent.

    Precondition:  0 <= percent <= 100.
    Postcondition: result is non-negative and rounded to cents.
    """
    if not 0.0 <= percent <= 100.0:
        raise ValueError(f"percent must be in [0, 100], got {percent}")
    result = round(price * (1 - percent / 100), 2)
    assert result >= 0.0, "postcondition: a discount cannot create a negative price"
    return result


@dataclass(frozen=True)
class Percent:
    """A parsed percentage: if one exists, it is valid. Parse, don't validate."""

    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 100.0:
            raise ValueError(f"percent must be in [0, 100], got {self.value}")


def discount(price: float, percent: Percent) -> float:
    """Takes an already-parsed Percent — the validity is guaranteed by its type."""
    return round(price * (1 - percent.value / 100), 2)
