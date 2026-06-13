"""Chapter 11 tests — Adapter and Façade, made executable.

Adapter: the wrapper genuinely translates (not just renames), fits our
interface, and a Protocol accepts a structural match without inheritance —
while the third-party adaptee does NOT match, which is why it needs the adapter.
Façade: one call drives the whole subsystem flow.
"""

import adapter
import facade
from adapter import (
    IPaymentGateway,
    InHouseGateway,
    Receipt,
    StripeClient,
    StripeGateway,
    SupportsCharge,
)


# --- Adapter ----------------------------------------------------------------

def test_adapter_translates_not_just_renames() -> None:
    gateway = StripeGateway(StripeClient())
    receipt = gateway.charge(10.0)
    assert isinstance(receipt, Receipt)
    assert receipt.provider == "stripe"
    assert receipt.confirmation == "ch_1000"  # $10.00 → 1000 cents
    assert receipt.amount == 10.0


def test_adapter_satisfies_our_interface() -> None:
    assert isinstance(StripeGateway(StripeClient()), IPaymentGateway)


def test_protocol_accepts_a_structural_match_without_inheritance() -> None:
    gateway = InHouseGateway()
    assert isinstance(gateway, SupportsCharge)       # matches by shape
    assert not isinstance(gateway, IPaymentGateway)  # never inherited it


def test_third_party_does_not_match_so_it_needs_the_adapter() -> None:
    # StripeClient has create_charge, not charge — structural mismatch
    assert not isinstance(StripeClient(), SupportsCharge)


# --- Façade -----------------------------------------------------------------

def test_facade_one_call_drives_the_flow() -> None:
    order = facade.Order([facade.LineItem("coffee", 100.0)])
    receipt = facade.place_order(order)
    assert receipt.total == 107.0            # 100 + 7% tax
    assert receipt.confirmation == "ch_10700"
