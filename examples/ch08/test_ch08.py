"""Chapter 8 tests — extension without modification, made executable.

Three claims:
  1. OCP: a gateway the core never knew about works without editing the core.
  2. Liskov: a single contract every substitute must satisfy — the compliant
     gateways pass it, the violator fails it.
  3. ABC is nominal (must inherit); Protocol is structural (matches by shape).
"""

import pytest

import after
import before
from after import (
    CardGateway,
    BadGateway,
    IPaymentGateway,
    PayPalGateway,
    Receipt,
    SupportsCharge,
    ThirdPartyWallet,
    process_payment,
)


# --- BEFORE works, but extension means editing the core ---------------------

def test_before_requires_editing_for_new_methods() -> None:
    assert before.process_payment("card", 10.0).provider == "card"
    with pytest.raises(ValueError):
        before.process_payment("crypto", 10.0)  # unknown until the function is edited


# --- OCP: extension without modification ------------------------------------

def test_new_gateway_needs_no_change_to_the_core() -> None:
    class CryptoGateway(IPaymentGateway):  # the core has never heard of this
        def charge(self, amount: float) -> Receipt:
            return Receipt("crypto", amount, f"btc-{int(amount * 100)}")

    receipt = process_payment(CryptoGateway(), 25.0)
    assert receipt.provider == "crypto"
    assert receipt.amount == 25.0


# --- Liskov: one contract every implementation must honor -------------------

GOOD_GATEWAYS = [CardGateway(), PayPalGateway(), ThirdPartyWallet()]


@pytest.mark.parametrize("gateway", GOOD_GATEWAYS)
def test_gateway_honors_the_charge_contract(gateway: object) -> None:
    receipt = gateway.charge(42.0)
    assert isinstance(receipt, Receipt)  # the postcondition the contract promises
    assert receipt.amount == 42.0


def test_bad_gateway_violates_the_contract() -> None:
    # inherits the ABC, so it type-checks — but breaks the promise at runtime
    assert not isinstance(BadGateway().charge(42.0), Receipt)


# --- ABC (nominal) vs Protocol (structural) ---------------------------------

def test_abc_is_nominal() -> None:
    assert isinstance(CardGateway(), IPaymentGateway)
    assert not isinstance(ThirdPartyWallet(), IPaymentGateway)  # never inherited it


def test_protocol_is_structural() -> None:
    # ThirdPartyWallet matches SupportsCharge by shape alone, no inheritance
    assert isinstance(ThirdPartyWallet(), SupportsCharge)
    assert isinstance(CardGateway(), SupportsCharge)
