// Chapter 6 tests — encapsulation made executable. Mirrors the Python suite:
// the before tests demonstrate the leaks the open object allows; the after tests
// prove the same illegal states are now impossible to reach.

import { describe, expect, it } from "vitest";
import { type LineItem } from "./models";
import * as before from "./before";
import * as after from "./after";

// --- BEFORE: the object cannot protect itself ------------------------------

describe("Before: nothing stops a caller from breaking it", () => {
  it("total goes stale", () => {
    const cart = new before.ShoppingCart();
    cart.items.push({ name: "coffee", price: 12.5 });
    // forgot to recompute(): total still claims 0
    expect(cart.total).toBe(0);
  });

  it("accepts a nonsense discount", () => {
    const cart = new before.ShoppingCart();
    cart.items.push({ name: "coffee", price: 10 });
    cart.discountRate = 2; // 200% off — accepted without complaint
    cart.recompute();
    expect(cart.total).toBe(-10); // a negative price, happily computed
  });
});

// --- AFTER: the same illegal states are unreachable ------------------------

describe("After: the illegal states are unrepresentable", () => {
  it("total is always correct (computed on read, cannot go stale)", () => {
    const cart = new after.ShoppingCart();
    cart.addItem({ name: "coffee", price: 12.5 });
    expect(cart.total).toBe(12.5);
  });

  it("rejects an invalid discount", () => {
    const cart = new after.ShoppingCart();
    expect(() => {
      cart.discountRate = 2;
    }).toThrow(RangeError);
  });

  it("total is read-only — assigning the computed value is both a type and a runtime error", () => {
    const cart = new after.ShoppingCart();
    expect(() => {
      // @ts-expect-error no setter for `total`; the lie does not type-check,
      // and in strict mode (ESM) the assignment throws at runtime too.
      cart.total = 999;
    }).toThrow(TypeError);
    expect(cart.total).toBe(0); // nothing changed
  });

  it("the items view cannot corrupt the cart", () => {
    const cart = new after.ShoppingCart();
    cart.addItem({ name: "coffee", price: 12.5 });
    const view = cart.items;
    // `view` is `readonly LineItem[]`: `.push` does not type-check, and the
    // returned copy is detached from the cart's private list anyway.
    const mutable = view as LineItem[];
    mutable.push({ name: "sneaky", price: 0 });
    expect(cart.total).toBe(12.5); // internal state untouched
  });

  it("the private fields are unreachable from outside", () => {
    const cart = new after.ShoppingCart();
    // `#items` is genuinely private — not even visible on the instance keys,
    // unlike Python's `_items`, which is only a convention.
    expect(Object.keys(cart)).not.toContain("items");
  });
});

// --- valid usage agrees across both designs --------------------------------

const CASES: ReadonlyArray<readonly [ReadonlyArray<readonly [string, number]>, number]> = [
  [
    [
      ["coffee", 12.5],
      ["mug", 7.5],
    ],
    0,
  ],
  [[["beans", 100]], 0.1],
  [[], 0.5],
];

describe("valid usage matches across both designs", () => {
  it.each(CASES)("prices=%j rate=%j", (prices, rate) => {
    const bc = new before.ShoppingCart();
    bc.items = prices.map(([name, price]): LineItem => ({ name, price }));
    bc.discountRate = rate;
    bc.recompute();

    const ac = new after.ShoppingCart();
    for (const [name, price] of prices) {
      ac.addItem({ name, price });
    }
    ac.discountRate = rate;

    expect(bc.total).toBe(ac.total);
  });
});
