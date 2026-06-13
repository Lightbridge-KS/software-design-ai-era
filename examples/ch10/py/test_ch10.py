"""Chapter 10 tests — factories and the demoted Singleton, made executable.

Claims:
  1. The factory builds the right concrete type per key, and fails fast on
     an unknown one (Chapter 7).
  2. Construction is centralized: every call site goes through make_gateway,
     and adding a provider is a single registry entry (open-closed).
  3. A module-level instance gives the one-instance guarantee with none of
     the Singleton-class machinery.
"""

import pytest

import after
import before
import singleton

METHODS = [("card", after.CardGateway), ("paypal", after.PayPalGateway)]


@pytest.mark.parametrize("method,cls", METHODS)
def test_factory_builds_the_right_type(method: str, cls: type) -> None:
    assert isinstance(after.make_gateway(method), cls)


def test_factory_fails_fast_on_unknown_method() -> None:
    with pytest.raises(ValueError, match="unknown payment method"):
        after.make_gateway("crypto")


def test_call_sites_preserve_behavior() -> None:
    a, b = after.checkout("card", 10.0), before.checkout("card", 10.0)
    assert (a.provider, a.amount) == (b.provider, b.amount)
    assert after.refund("paypal", 5.0).amount == -5.0


def test_registry_is_the_single_growth_point() -> None:
    class CryptoGateway(after.IPaymentGateway):
        def charge(self, amount: float) -> after.Receipt:
            return after.Receipt("crypto", amount)

    after._GATEWAYS["crypto"] = CryptoGateway  # one entry — no other code changes
    try:
        assert isinstance(after.make_gateway("crypto"), CryptoGateway)
    finally:
        del after._GATEWAYS["crypto"]


def test_module_level_instance_is_shared() -> None:
    import singleton as also_singleton  # same cached module object

    assert singleton.pool is also_singleton.pool  # one instance, no machinery


def test_singleton_class_offers_nothing_extra() -> None:
    # The pattern works — but the module-level instance already gave us this.
    assert singleton.SingletonPool() is singleton.SingletonPool()
