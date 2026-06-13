// Chapter 11 tests — Adapter and Façade, made executable. Mirrors the Python suite.
//
// Adapter: the wrapper genuinely translates (not just renames), fits our
// interface, and a structural shape accepts a matching object without
// inheritance — while the third-party adaptee does NOT match, which is why it
// needs the adapter. Façade: one call drives the whole subsystem flow.

import { describe, expect, it } from "vitest";
import {
  type Receipt,
  type SupportsCharge,
  InHouseGateway,
  StripeClient,
  StripeGateway,
} from "./adapter";
import { type Order, type LineItem, placeOrder } from "./facade";

// A structural check: does this value have a callable `charge`? This is the
// runtime stand-in for Python's `isinstance(x, SupportsCharge)` — TS erases the
// interface at compile time, so structural conformance is checked by shape.
const supportsCharge = (x: unknown): x is SupportsCharge =>
  typeof (x as { charge?: unknown }).charge === "function";

// --- Adapter ----------------------------------------------------------------

describe("Adapter: translates, not just renames", () => {
  it("converts dollars to cents and a record to a Receipt", () => {
    const gateway = new StripeGateway(new StripeClient());
    const receipt: Receipt = gateway.charge(10);
    expect(receipt.provider).toBe("stripe");
    expect(receipt.confirmation).toBe("ch_1000"); // $10.00 → 1000 cents
    expect(receipt.amount).toBe(10);
  });
});

describe("Adapter: structural shape accepts a match without inheritance", () => {
  it("an in-house class already shaped like SupportsCharge needs no adapter", () => {
    expect(supportsCharge(new InHouseGateway())).toBe(true);
  });

  it("the third-party SDK does NOT match, so it needs the adapter", () => {
    // StripeClient has createCharge, not charge — structural mismatch.
    expect(supportsCharge(new StripeClient())).toBe(false);
  });
});

// --- Façade -----------------------------------------------------------------

describe("Façade: one call drives the flow", () => {
  it("places an order through all four subsystems", () => {
    const item: LineItem = { name: "coffee", price: 100 };
    const order: Order = { items: [item] };
    const receipt = placeOrder(order);
    expect(receipt.total).toBe(107); // 100 + 7% tax
    expect(receipt.confirmation).toBe("ch_10700");
  });
});
