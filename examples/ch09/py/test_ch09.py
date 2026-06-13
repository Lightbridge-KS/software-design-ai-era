"""Chapter 9 tests — the same behavioral contract, run against both designs.

The point the tests make: the cathedral and the two functions are
behaviorally identical. Everything the cathedral adds is structure the
contract never asked for.
"""

from pathlib import Path

import pytest

import after_simple
import before_cathedral
from models import LineItem, Order

ORDERS = [
    Order(items=[LineItem("coffee", 12.50), LineItem("mug", 7.50)]),
    Order(items=[LineItem("beans", 18.00)], is_member=True),
    Order(),  # empty order: the edge case both designs must honor
]


def cathedral_roundtrip(orders: list[Order], path: Path) -> list[Order]:
    settings = before_cathedral.StorageSettings(
        storage_dir=str(path.parent), filename=path.name
    )
    repo = before_cathedral.JsonOrderRepository(settings)
    repo.save(orders)
    return repo.load()


def simple_roundtrip(orders: list[Order], path: Path) -> list[Order]:
    after_simple.save_orders(orders, path)
    return after_simple.load_orders(path)


@pytest.mark.parametrize("roundtrip", [cathedral_roundtrip, simple_roundtrip])
def test_roundtrip_preserves_orders(roundtrip, tmp_path: Path) -> None:
    path = tmp_path / "orders.json"
    assert roundtrip(ORDERS, path) == ORDERS


def test_both_designs_write_identical_files(tmp_path: Path) -> None:
    cathedral_path = tmp_path / "cathedral.json"
    simple_path = tmp_path / "simple.json"
    cathedral_roundtrip(ORDERS, cathedral_path)
    simple_roundtrip(ORDERS, simple_path)
    assert cathedral_path.read_text() == simple_path.read_text()


def test_factory_produces_its_one_and_only_type(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("ORDERS_STORAGE_DIR", str(tmp_path))
    repo = before_cathedral.OrderRepositoryFactory.create()
    assert isinstance(repo, before_cathedral.JsonOrderRepository)
