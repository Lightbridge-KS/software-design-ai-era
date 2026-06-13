"""Chapter 4 · BEFORE: one function, four actors.

checkout() changes for four unrelated reasons — finance (tax), ops
(shipping), marketing (email copy), engineering (storage). That is four
reasons to change in one body: the structural definition of "does too much".
"""

import json
import smtplib
from email.message import EmailMessage
from pathlib import Path

from models import Order

ORDERS_FILE = Path("orders.json")


def checkout(order: Order, payment_token: str, send_email: bool = True) -> float:
    total = order.subtotal
    if order.customer.is_member:
        total = total * 0.85

    if order.country == "US":
        total = total + total * 0.07
    elif order.country == "DE":
        total = total + total * 0.19
    elif order.country == "JP":
        total = total + total * 0.10

    if order.country == "US":
        total = total + 5.00
    elif order.country in ("DE", "FR", "NL"):
        total = total + 9.90
    else:
        total = total + 24.90
    if order.gift_wrap:
        total = total + 3.50

    total = round(total, 2)
    print(f"Charging {payment_token} for {total:.2f}")

    if order.customer.is_member and send_email:
        msg = EmailMessage()
        msg["Subject"] = "Your checkout-lite receipt"
        msg["To"] = order.customer.email
        msg.set_content(f"Thanks {order.customer.name}! You paid {total:.2f}.")
        try:
            with smtplib.SMTP("localhost", 25, timeout=1) as smtp:
                smtp.send_message(msg)
        except OSError:
            pass

    record = {"customer": order.customer.name, "total": total}
    existing = json.loads(ORDERS_FILE.read_text()) if ORDERS_FILE.exists() else []
    existing.append(record)
    ORDERS_FILE.write_text(json.dumps(existing, indent=2))
    return total
