// Chapter 8 tests — extension without modification, made executable.
// Mirrors the Python suite. Three claims:
//   1. OCP: a gateway the core never knew about works without editing the core.
//   2. Liskov: a single contract every substitute must satisfy — the compliant
//      gateways pass it, the violator fails it.
//   3. Nominal vs structural: Python makes you choose (ABC vs Protocol); in TS
//      interfaces are structural, so a class with the right shape satisfies the
//      interface WITHOUT `implements` — and so does a foreign object.

import { describe, expect, it } from "vitest";
import * as before from "./before";
import {
  type IPaymentGateway,
  type Receipt,
  BadGateway,
  CardGateway,
  InHouseGateway,
  PayPalGateway,
  processPayment,
  thirdPartyWallet,
} from "./after";

// --- BEFORE works, but extension means editing the core ---------------------

describe("Before: extension requires editing the core", () => {
  it("handles the methods baked into the switch", () => {
    expect(before.processPayment("card", 10).provider).toBe("card");
  });

  it("rejects anything not yet coded into the function", () => {
    expect(() => before.processPayment("crypto", 10)).toThrow();
  });
});

// --- OCP: extension without modification ------------------------------------

describe("OCP: a new gateway needs no change to the core", () => {
  it("flows a gateway the core has never heard of through processPayment", () => {
    // Defined right here, never imported by the core — yet it just works.
    class CryptoGateway implements IPaymentGateway {
      charge(amount: number): Receipt {
        return { provider: "crypto", amount, confirmation: `btc-${Math.round(amount * 100)}` };
      }
    }

    const receipt = processPayment(new CryptoGateway(), 25);
    expect(receipt.provider).toBe("crypto");
    expect(receipt.amount).toBe(25);
  });
});

// --- Liskov: one contract every implementation must honor -------------------

// The contract the base promises: charge(amount) returns a Receipt for amount.
const honorsChargeContract = (gateway: IPaymentGateway): boolean => {
  const receipt = gateway.charge(42) as Receipt | null;
  return receipt !== null && typeof receipt === "object" && receipt.amount === 42;
};

describe("Liskov: substitutes share one contract", () => {
  const goodGateways: ReadonlyArray<[string, IPaymentGateway]> = [
    ["card", new CardGateway()],
    ["paypal", new PayPalGateway()],
    ["inhouse", new InHouseGateway()], // no `implements`, fits structurally
    ["wallet", thirdPartyWallet], // a plain object, fits structurally
  ];

  it.each(goodGateways)("%s gateway honors the charge contract", (_name, gateway) => {
    expect(honorsChargeContract(gateway)).toBe(true);
  });

  it("a BadGateway type-checks but breaks the contract at runtime", () => {
    expect(honorsChargeContract(new BadGateway())).toBe(false);
  });
});

// --- Nominal vs structural --------------------------------------------------

// A runtime stand-in for "does this value satisfy the interface?". TS erases
// interfaces at compile time, so structural conformance is checked by shape —
// this is the analogue of Python's `isinstance(x, SupportsCharge)`.
const supportsCharge = (x: unknown): x is IPaymentGateway =>
  typeof (x as { charge?: unknown }).charge === "function";

describe("Structural by default: shape, not name, decides conformance", () => {
  it("InHouseGateway satisfies the interface without `implements`", () => {
    const gateway: IPaymentGateway = new InHouseGateway(); // assignable by shape
    expect(supportsCharge(gateway)).toBe(true);
    expect(gateway.charge(5).provider).toBe("inhouse");
  });

  it("a foreign object literal satisfies it too — no class, no inheritance", () => {
    expect(supportsCharge(thirdPartyWallet)).toBe(true);
  });

  it("a value with the wrong shape does NOT satisfy it", () => {
    expect(supportsCharge({ pay: () => null })).toBe(false);
  });
});
