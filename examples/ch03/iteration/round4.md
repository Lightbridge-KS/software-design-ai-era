**The fix:** `member_discount` is now computed as `round(subtotal - discounted, 2)` — derived from the already-rounded `discounted`, not from `raw_discounted`. Since both `subtotal` and `discounted` are rounded to 2 dp before this subtraction, the result is exact and the identity `subtotal - member_discount == discounted` holds by construction.

**The test:** two assertions per case:
- `discounted + tax + shipping == total` — the bottom-line reconciliation from the previous fix
- `round(subtotal - member_discount, 2) == discounted` — the new discount-line reconciliation

Six cases span member/non-member, US/EU/JP/unknown-country, with and without gift wrap, including the original edge case (`[0.04]`, US member) that caught the first bug.
