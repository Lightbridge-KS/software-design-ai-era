Done. Here's what changed:

**`models.py`** — added `PricingBreakdown` (lines 31–38): a frozen dataclass with six fields covering every line of the receipt. `member_discount` stores the savings *amount* (e.g. `7.50`), not the rate, so the display layer can render `- $7.50` directly.

**`pricing.py`** — added `price_order` (lines 30–45) as the new primary function. It calls the three existing helpers unchanged, captures each intermediate, and packages them into `PricingBreakdown`. `order_total` (lines 48–50) is now a one-line shim — same signature, same result, no behavior change for existing callers.
