Done — `discounts.py` is refactored in place and all behavior checks pass, including the empty-order, non-member, and coupon-floor edge cases.

What changed:

- **Replaced the `if/elif` chain with a registry** (`_DISCOUNTS: dict[str, DiscountFn]`). Each discount is now a small named function, and `apply_discount` just looks up and delegates. Adding a discount is one function plus one dict entry — no editing of dispatch logic.
- **Added a `DiscountFn` type alias** (`Callable[[Order], float]`) so the contract for a discount rule is explicit.
- **Better error message**: unknown kinds now raise `ValueError: unknown discount: 'bogus' (expected one of: coupon5, member, none, ten_percent)` instead of just echoing the bad value.
- Public API (`LineItem`, `Order`, `apply_discount`) and all results are unchanged.

One thing I left alone deliberately: prices are still `float`. That's fine for a demo, but real money math accumulates rounding errors — `Decimal` (or integer cents) would be the production-grade fix, and it would change the public types.

Would you like me to add a small `pytest` test file covering these cases, or switch the money representation to `Decimal`?
