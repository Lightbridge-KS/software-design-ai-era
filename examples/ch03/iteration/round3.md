Two things changed:

1. **`discounted`, `tax`, `shipping` are rounded before `total` is computed.** `total = round(discounted + tax + shipping, 2)` now sums the same numbers that go into the struct — so the receipt always adds up.

2. **`tax_for` still receives `raw_discounted`** (the unrounded discount base), not the already-rounded `discounted`. This is intentional: tax is a legal charge computed on the actual discounted amount, not on a display-rounded approximation. The rounding that matters for consistency is applied *after* the rate math, not before it.
