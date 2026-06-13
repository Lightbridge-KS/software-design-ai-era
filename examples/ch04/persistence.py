"""Persistence — answers to one actor: engineering (how orders are stored).

One reason to change: the storage format. Change to a database and only this
module moves.
"""

import json
from pathlib import Path

from models import Order

ORDERS_FILE = Path("orders.json")


def save_order(order: Order, total: float) -> None:
    record = {"customer": order.customer.name, "total": total}
    existing = json.loads(ORDERS_FILE.read_text()) if ORDERS_FILE.exists() else []
    existing.append(record)
    ORDERS_FILE.write_text(json.dumps(existing, indent=2))
