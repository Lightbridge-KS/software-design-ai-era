import pytest
from models import Customer, LineItem, Order
from pricing import price_order

MEMBER = Customer("Alice", "a@example.com", is_member=True)
GUEST  = Customer("Bob",   "b@example.com", is_member=False)

CASES = [
    (MEMBER, [0.04],          "US", False),
    (MEMBER, [30.00, 20.00],  "US", True),
    (GUEST,  [99.99],         "DE", False),
    (GUEST,  [10.00],         "JP", True),
    (MEMBER, [0.01],          "FR", False),
    (GUEST,  [150.00],        "AU", False),  # unknown country → no tax
]


@pytest.mark.parametrize("customer,prices,country,gift_wrap", CASES)
def test_breakdown_is_internally_consistent(customer, prices, country, gift_wrap):
    order = Order(
        customer=customer,
        items=[LineItem(f"item{i}", p) for i, p in enumerate(prices)],
        country=country,
        gift_wrap=gift_wrap,
    )
    b = price_order(order)
    assert b.discounted + b.tax + b.shipping == b.total
    assert round(b.subtotal - b.member_discount, 2) == b.discounted
