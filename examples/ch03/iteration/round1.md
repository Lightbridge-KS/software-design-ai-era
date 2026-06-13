Here's the design proposal.

---

## Proposed Design

### The gap

`order_total` in `pricing.py` returns one `float` — the final total. The computation already does everything needed (discount, tax, shipping), but discards the intermediate values. We need a way to surface those intermediates to the caller without duplicating the math.

---

### New: `PricingBreakdown` dataclass (in `models.py`)

```python
@dataclass(frozen=True)
class PricingBreakdown:
    subtotal:          float   # sum of item prices
    member_discount:   float   # discount amount (negative savings); 0 if not a member
    discounted:        float   # subtotal after discount
    tax:               float   # tax amount
    shipping:          float   # shipping + gift-wrap
    total:             float   # final charge
```

A plain frozen dataclass — same philosophy as `Order` and `LineItem`. The caller can display any or all fields; serializing to JSON or a receipt template is trivial.

**Why `discount` as an amount, not a rate?** The display layer wants to show `- $4.50`, not `- 15%`. The rate is an implementation detail of `pricing.py`.

---

### New: `price_order(order: Order) -> PricingBreakdown` (in `pricing.py`)

```python
def price_order(order: Order) -> PricingBreakdown:
```

This replaces `order_total` as the primary entry point. It calls the same three helpers (`member_discount`, `tax_for`, `shipping_for`) and packages their results into `PricingBreakdown`.

`order_total` can then become a one-liner that delegates:

```python
def order_total(order: Order) -> float:
    return price_order(order).total   # backward-compatible shim
```

---

### Relationship to existing code

```
price_order(order)          ← new primary function
  ├── member_discount(...)  ← unchanged
  ├── tax_for(...)          ← unchanged
  ├── shipping_for(...)     ← unchanged
  └── returns PricingBreakdown

order_total(order)          ← kept as shim → price_order().total
```

The three helper functions stay exactly as they are. The only additions are the `PricingBreakdown` dataclass and `price_order`. No existing code breaks.

---

### Main tradeoff to consider

The alternative is to return a plain `dict` instead of a dataclass, which requires less ceremony. The dataclass wins here because it gives type-checked field access, IDE autocomplete, and is consistent with how `Order` / `Customer` / `LineItem` are modelled — same style, same safety.

Want me to implement this?
