"""Chapter 9 · BEFORE: the cathedral.

Three hundred-ish lines (in spirit) answering a thirty-line question:
"save completed orders to disk so we can reload them later."

Every piece is individually defensible. The sum is not. Each class below is
annotated with the future it speculates about — none of which was requested.
"""

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from models import LineItem, Order


@dataclass(frozen=True)
class StorageSettings:
    """Speculates: paths will need environment-based configuration someday."""

    storage_dir: str
    filename: str

    @classmethod
    def from_env(cls) -> "StorageSettings":
        return cls(
            storage_dir=os.environ.get("ORDERS_STORAGE_DIR", "."),
            filename=os.environ.get("ORDERS_FILENAME", "orders.json"),
        )


class LineItemSerializer:
    """Speculates: line-item serialization will vary someday."""

    def to_dict(self, item: LineItem) -> dict[str, object]:
        return {"name": item.name, "price": item.price}

    def from_dict(self, data: dict[str, object]) -> LineItem:
        return LineItem(name=str(data["name"]), price=float(data["price"]))  # type: ignore[arg-type]


class OrderSerializer:
    """Speculates: order serialization will vary someday."""

    def __init__(self) -> None:
        self._item_serializer = LineItemSerializer()

    def to_dict(self, order: Order) -> dict[str, object]:
        return {
            "items": [self._item_serializer.to_dict(i) for i in order.items],
            "is_member": order.is_member,
        }

    def from_dict(self, data: dict[str, object]) -> Order:
        return Order(
            items=[self._item_serializer.from_dict(d) for d in data["items"]],  # type: ignore[union-attr]
            is_member=bool(data["is_member"]),
        )


class IOrderRepository(ABC):
    """Speculates: a second storage backend someday."""

    @abstractmethod
    def save(self, orders: list[Order]) -> None: ...

    @abstractmethod
    def load(self) -> list[Order]: ...


class JsonOrderRepository(IOrderRepository):
    """The interface's only implementation — and no second in sight."""

    def __init__(self, settings: StorageSettings) -> None:
        self._path = Path(settings.storage_dir) / settings.filename
        self._serializer = OrderSerializer()

    def save(self, orders: list[Order]) -> None:
        payload = [self._serializer.to_dict(o) for o in orders]
        self._path.write_text(json.dumps(payload, indent=2))

    def load(self) -> list[Order]:
        payload = json.loads(self._path.read_text())
        return [self._serializer.from_dict(d) for d in payload]


class OrderRepositoryFactory:
    """A factory that can only ever produce one type."""

    @staticmethod
    def create(kind: str = "json") -> IOrderRepository:
        if kind == "json":
            return JsonOrderRepository(StorageSettings.from_env())
        raise ValueError(f"unknown repository kind: {kind}")
