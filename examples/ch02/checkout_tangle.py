"""Chapter 2 · The Disaster.

This is what checkout() became after four innocent change requests, each a
reasonable two-minute edit on its own:

    1. "Charge the customer."          -> pricing
    2. "We owe sales tax now."         -> + tax, branched by country
    3. "Add shipping costs."           -> + shipping, branched by country
    4. "Email members their receipt."  -> + notification
    5. "Save completed orders."        -> + persistence

Every step was locally reasonable. The sum is a knot: pricing, tax, shipping,
notification, and persistence are braided into one body. The code WORKS — that
is the point. It is bad design, not broken code. Chapter 2 diagnoses it; the
rest of the book takes it apart.
"""

import json
import smtplib
from email.message import EmailMessage
from pathlib import Path

from models import Order

ORDERS_FILE = Path("orders.json")


def checkout(order: Order, payment_token: str, send_email: bool = True) -> float:
    # --- pricing -------------------------------------------------------------
    total = order.subtotal
    if order.customer.is_member:
        total = total * 0.85

    # --- tax (grew a branch per country) -------------------------------------
    if order.country == "US":
        total = total + total * 0.07
    elif order.country == "DE":
        total = total + total * 0.19
    elif order.country == "JP":
        total = total + total * 0.10
    # other countries: no tax (that we know of...)

    # --- shipping (another branch per country) -------------------------------
    if order.country == "US":
        total = total + 5.00
    elif order.country in ("DE", "FR", "NL"):
        total = total + 9.90
    else:
        total = total + 24.90
    if order.gift_wrap:
        total = total + 3.50

    # --- take payment --------------------------------------------------------
    print(f"Charging {payment_token} for {total:.2f}")  # pretend gateway call

    # --- notification (only members, only sometimes) -------------------------
    if order.customer.is_member and send_email:
        msg = EmailMessage()
        msg["Subject"] = "Your checkout-lite receipt"
        msg["To"] = order.customer.email
        msg.set_content(f"Thanks {order.customer.name}! You paid {total:.2f}.")
        try:
            with smtplib.SMTP("localhost", 25, timeout=1) as smtp:
                smtp.send_message(msg)
        except OSError:
            pass  # swallow: we don't want email to block a sale

    # --- persistence (braided right in at the end) ---------------------------
    record = {
        "customer": order.customer.name,
        "items": [{"name": i.name, "price": i.price} for i in order.items],
        "country": order.country,
        "total": round(total, 2),
    }
    existing = json.loads(ORDERS_FILE.read_text()) if ORDERS_FILE.exists() else []
    existing.append(record)
    ORDERS_FILE.write_text(json.dumps(existing, indent=2))

    return round(total, 2)
