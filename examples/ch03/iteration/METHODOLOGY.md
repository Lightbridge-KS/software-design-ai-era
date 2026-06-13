# The Worked Iteration — Methodology

The four-round dialogue in Chapter 3 is real, not authored. This file records how
it was produced, so the iteration is reproducible.

## Setup

- **Starter:** `starter/` — checkout-lite's `models.py` and a clean `pricing.py`
  with composable rate logic (`member_discount`, `tax_for`, `shipping_for`,
  `order_total`). A deliberately clean starting point: the chapter teaches the
  loop on *new* code, not on an existing tangle.
- **Task:** add an itemized cost breakdown (subtotal, member discount, tax,
  shipping, total) for display to customers.
- **Agent:** Claude Code, non-interactive (`claude -p`), **`--model sonnet`** —
  a deliberately less capable model than the author's default, chosen to see
  whether the loop's value survives a weaker partner. Session continuity across
  rounds via `--continue`; file edits auto-accepted from Round 2 on.
- **The human in the loop** was the book's author agent, reviewing each real
  output and writing the next prompt as a developer would — Rounds 3 and 4
  genuinely depended on what Rounds 1 and 2 produced.

## The rounds (verbatim agent replies in `round1.md` … `round4.md`)

1. **intend → express.** *Propose a design before coding.* The guide worked:
   Sonnet proposed a structured `PricingBreakdown` dataclass reusing the existing
   helpers, with `order_total` kept as a shim — not the formatted-string tangle a
   code-first prompt might have produced.
2. **generate → review.** Implementation matched the proposal, but introduced a
   silent defect: each field was rounded independently while `total` came from the
   unrounded values, so the receipt's own lines did not always sum to its total
   (e.g. a $0.04 US member order showed 0.03 + 0.00 + 5.00 = 5.03 but total 5.04).
   Review caught what the guide could not anticipate.
3. **refine.** Redirected on the bug. Sonnet rounded the components before summing
   and, thoughtfully, kept tax computed on the unrounded base (a legal charge, not
   a display approximation). The bottom line reconciled; a residual remained on the
   discount line.
4. **review → accept.** Redirected on the residual, and asked for a test asserting
   the reconciliation invariant — promoting the recurring "it must add up" concern
   from a one-off catch into a persistent sensor. Accepted.

## Result

`final/` holds the accepted `models.py`, `pricing.py`, and `test_pricing.py`. The
invariants (`discounted + tax + shipping == total` and
`subtotal - member_discount == discounted`) hold across thousands of generated
cases; the test passes.

The chapter may trim replies for length; trims are marked `[…]`. Nothing else is
edited.
