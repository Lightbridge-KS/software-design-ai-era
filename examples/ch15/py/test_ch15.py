"""Chapter 15 tests — Iterator and Visitor, made executable.

Iterator: a catalog iterates without exposing its list, and a generator streams
batches. Visitor: two operations walk the same Chapter-12 tree, and the match
replacement agrees with the classical visitor.
"""

from catalog import Catalog, Product, paged
from visitor import (
    Bundle,
    CountItemsVisitor,
    Product as LineProduct,
    TotalPriceVisitor,
    total_via_match,
)


# --- Iterator ---------------------------------------------------------------

def test_catalog_is_iterable_without_exposing_its_list() -> None:
    catalog = Catalog([Product("mug", 12.0), Product("pen", 3.0)])
    names = [p.name for p in catalog]  # a for-loop, no get_items()
    assert names == ["mug", "pen"]
    assert len(catalog) == 2


def test_paged_streams_fixed_size_batches() -> None:
    products = [Product(str(i), float(i)) for i in range(5)]
    batches = list(paged(products, size=2))
    assert [len(batch) for batch in batches] == [2, 2, 1]


# --- Visitor ----------------------------------------------------------------

def _tree() -> Bundle:
    return Bundle("kit", [
        LineProduct("mug", 12.0),
        Bundle("duo", [LineProduct("light", 9.0), LineProduct("dark", 9.0)]),
    ])


def test_total_price_visitor_walks_the_tree() -> None:
    assert _tree().accept(TotalPriceVisitor()) == 30.0


def test_count_items_visitor_reuses_the_same_tree() -> None:
    assert _tree().accept(CountItemsVisitor()) == 3


def test_match_replacement_agrees_with_the_visitor() -> None:
    tree = _tree()
    assert total_via_match(tree) == tree.accept(TotalPriceVisitor())
