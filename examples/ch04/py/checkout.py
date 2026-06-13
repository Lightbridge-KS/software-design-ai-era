"""Checkout — answers to one actor: the order workflow itself.

One reason to change: the *sequence* of steps. It owns orchestration, not
the steps' internals. Each concern lives in its own cohesive module; this
function reads like a table of contents.
"""

import pricing
import notify
import persistence
from models import Order


def checkout(order: Order, payment_token: str, send_email: bool = True) -> float:
    total = pricing.order_total(order)
    print(f"Charging {payment_token} for {total:.2f}")
    if order.customer.is_member and send_email:
        notify.send_receipt(order, total)
    persistence.save_order(order, total)
    return total
