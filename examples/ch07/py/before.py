"""Chapter 7 · BEFORE: a function that breaks its own promise.

The name says "discount" but the units are unstated, and nothing is checked.
Pass 0.2 meaning "20%" and you get a 0.2% discount; pass 150 and you get a
negative price that flows downstream and detonates somewhere far away.
"""


def apply_discount(price: float, percent: float) -> float:
    return price - price * percent / 100
