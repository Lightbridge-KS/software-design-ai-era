"""Notification — answers to one actor: marketing (the receipt message).

One reason to change: what the customer is told, and how. The email I/O is
isolated here, away from the money math.
"""

import smtplib
from email.message import EmailMessage

from models import Order


def receipt_body(order: Order, total: float) -> str:
    """Pure: the message text. Marketing owns this; no I/O to test around."""
    return f"Thanks {order.customer.name}! You paid {total:.2f}."


def send_receipt(order: Order, total: float) -> None:
    """The I/O edge. Failures never block a sale."""
    msg = EmailMessage()
    msg["Subject"] = "Your checkout-lite receipt"
    msg["To"] = order.customer.email
    msg.set_content(receipt_body(order, total))
    try:
        with smtplib.SMTP("localhost", 25, timeout=1) as smtp:
            smtp.send_message(msg)
    except OSError:
        pass
