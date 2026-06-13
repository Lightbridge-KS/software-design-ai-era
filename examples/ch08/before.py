"""Chapter 8 · BEFORE: closed for extension, open for modification — backwards.

Every new payment provider means editing process_payment — the one function
you least want to touch, and the one whose existing branches you most risk
breaking.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Receipt:
    provider: str
    amount: float
    confirmation: str


def process_payment(method: str, amount: float) -> Receipt:
    if method == "card":
        return Receipt("card", amount, f"card-{int(amount * 100)}")
    elif method == "paypal":
        return Receipt("paypal", amount, f"pp-{int(amount * 100)}")
    else:
        raise ValueError(f"unknown payment method: {method}")
