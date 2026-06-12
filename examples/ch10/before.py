"""Chapter 10 · BEFORE: the tangle.

Several algorithms trapped in one body — every new discount rule edits
apply_discount, and the two receipt renderers duplicate the same skeleton.
"""

from models import Order


def apply_discount(order: Order, kind: str) -> float:
    """Return the order total after the given discount."""
    if kind == "none":
        return order.subtotal
    elif kind == "ten_percent":
        return order.subtotal * 0.90
    elif kind == "coupon5":
        return max(order.subtotal - 5.00, 0.0)
    elif kind == "member":
        if order.is_member:
            return order.subtotal * 0.85
        return order.subtotal
    else:
        raise ValueError(f"unknown discount: {kind}")


def render_text_receipt(order: Order) -> str:
    lines = ["CHECKOUT-LITE RECEIPT"]                  # header
    for item in order.items:                           # line items
        lines.append(f"{item.name:<20} {item.price:>8.2f}")
    lines.append(f"Total: {order.subtotal:.2f}")       # footer
    return "\n".join(lines)


def render_html_receipt(order: Order) -> str:
    rows = "".join(
        f"<tr><td>{item.name}</td><td>{item.price:.2f}</td></tr>"
        for item in order.items
    )
    return "\n".join([
        "<h1>Checkout-lite receipt</h1>",              # header
        f"<table>{rows}</table>",                      # line items
        f"<p>Total: {order.subtotal:.2f}</p>",         # footer — same shape, duplicated
    ])
