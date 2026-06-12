Done. `apply_discount` in `discounts.py` is now Strategy-pattern based, verified with a quick behavioral check covering all four discount kinds, the zero-floor on `coupon5`, the member/non-member branch, and the unknown-kind `ValueError` — all passed.

What changed:

- Each branch of the old if/elif chain became a small strategy function: `_no_discount`, `_ten_percent`, `_coupon5`, `_member`, each with the signature `(Order) -> float`.
- A registry dict `_DISCOUNT_STRATEGIES: dict[str, Callable[[Order], float]]` maps each kind string to its strategy.
- `apply_discount(order, kind)` keeps its exact signature and docstring; it now looks up the strategy and dispatches, re-raising a `KeyError` as the same `ValueError(f"unknown discount: {kind}")` as before (with `from None` so the traceback stays clean).
- Added one import: `from collections.abc import Callable`.

Adding a new discount is now a one-function + one-registry-entry change, with no edits to `apply_discount` itself.
