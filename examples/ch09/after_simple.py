"""Chapter 9 · AFTER: right-sized.

Same behavior as the cathedral; roughly eighty percent less code.
The `path` parameter is the flexibility the settings system promised —
a function argument is the cheapest seam there is.
"""

import json
from pathlib import Path

from models import LineItem, Order


def save_orders(orders: list[Order], path: Path) -> None:
    payload = [
        {
            "items": [{"name": i.name, "price": i.price} for i in o.items],
            "is_member": o.is_member,
        }
        for o in orders
    ]
    path.write_text(json.dumps(payload, indent=2))


def load_orders(path: Path) -> list[Order]:
    return [
        Order(
            items=[LineItem(**item) for item in entry["items"]],
            is_member=entry["is_member"],
        )
        for entry in json.loads(path.read_text())
    ]
