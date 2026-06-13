"""Chapter 12 tests — Composite and Decorator, made executable.

Composite: leaf and bundle answer price() uniformly, and a bundle recurses into
a nested bundle. Decorator: behavior wraps the gateway without editing it, and
decorators stack at runtime while preserving the interface.
"""

from bundle import Bundle, LineItem, Product, cart_total
from gateway_decorators import (
    IPaymentGateway,
    LoggingGateway,
    Receipt,
    RetryingGateway,
    StripeGateway,
    TransientError,
)


# --- Composite --------------------------------------------------------------

def test_bundle_prices_itself_by_recursing() -> None:
    kit = Bundle("starter-kit", [
        Product("mug", 12.0),
        Bundle("beans-duo", [Product("light", 9.0), Product("dark", 9.0)]),
    ])
    assert kit.price() == 30.0  # 12 + (9 + 9) — one real nested level


def test_cart_totals_leaves_and_bundles_uniformly() -> None:
    items: list[LineItem] = [
        Product("mug", 12.0),
        Bundle("duo", [Product("a", 3.0), Product("b", 4.0)]),
    ]
    assert cart_total(items) == 19.0


def test_leaf_and_composite_share_the_interface() -> None:
    assert isinstance(Product("x", 1.0), LineItem)
    assert isinstance(Bundle("b"), LineItem)


# --- Decorator --------------------------------------------------------------

def test_logging_wraps_the_delegated_charge() -> None:
    log: list[str] = []
    gateway: IPaymentGateway = LoggingGateway(StripeGateway(), log)
    receipt = gateway.charge(10.0)
    assert receipt.confirmation == "ch_1000"
    assert log == ["charging 10.00", "charged ch_1000"]


def test_retry_recovers_from_transient_failure() -> None:
    calls = {"n": 0}

    class Flaky(IPaymentGateway):
        def charge(self, amount: float) -> Receipt:
            calls["n"] += 1
            if calls["n"] < 3:
                raise TransientError("try again")
            return Receipt("flaky", amount, "ok")

    gateway = RetryingGateway(Flaky(), retries=2)
    assert gateway.charge(5.0).confirmation == "ok"
    assert calls["n"] == 3


def test_decorators_stack_at_runtime() -> None:
    log: list[str] = []
    gateway = RetryingGateway(LoggingGateway(StripeGateway(), log))
    assert gateway.charge(20.0).confirmation == "ch_2000"
    assert log == ["charging 20.00", "charged ch_2000"]
