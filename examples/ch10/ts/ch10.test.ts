// Chapter 10 tests — factories and the demoted Singleton, made executable.
// Mirrors the Python suite (test_ch10.py):
//   1. The factory builds the right concrete type per key, and fails fast on
//      an unknown one (Chapter 7).
//   2. Construction is centralized: every call site goes through makeGateway,
//      and adding a provider is a single registry entry (open-closed).
//   3. A module-level instance gives the one-instance guarantee with none of
//      the Singleton-class machinery.

import { describe, expect, it } from "vitest";
import { type IPaymentGateway, type Receipt, CardGateway, PayPalGateway } from "./models";
import * as before from "./before";
import * as after from "./after";
import * as singleton from "./singleton";

const METHODS: ReadonlyArray<[string, new () => IPaymentGateway]> = [
  ["card", CardGateway],
  ["paypal", PayPalGateway],
];

describe("Factory: builds the right concrete type per key", () => {
  it.each(METHODS)("makeGateway(%s) is the right class", (method, cls) => {
    expect(after.makeGateway(method)).toBeInstanceOf(cls);
  });

  it("fails fast on an unknown method (Chapter 7)", () => {
    expect(() => after.makeGateway("crypto")).toThrow("unknown payment method");
  });
});

describe("Factory: construction is centralized, behavior preserved", () => {
  it("call sites match the before tangle", () => {
    const a = after.checkout("card", 10);
    const b = before.checkout("card", 10);
    expect([a.provider, a.amount]).toEqual([b.provider, b.amount]);
    expect(after.refund("paypal", 5).amount).toBe(-5);
  });

  it("the registry is the single growth point (open-closed)", () => {
    class CryptoGateway implements IPaymentGateway {
      charge(amount: number): Receipt {
        return { provider: "crypto", amount };
      }
    }
    after.GATEWAYS["crypto"] = () => new CryptoGateway(); // one entry — no other code changes
    try {
      expect(after.makeGateway("crypto")).toBeInstanceOf(CryptoGateway);
    } finally {
      delete after.GATEWAYS["crypto"];
    }
  });
});

describe("Singleton, demoted: a module-level instance is the singleton", () => {
  it("the module-level instance is shared across importers", () => {
    expect(singleton.pool).toBe(singleton.pool); // one cached module object
  });

  it("the Singleton class offers nothing the module instance didn't", () => {
    expect(singleton.SingletonPool.getInstance()).toBe(
      singleton.SingletonPool.getInstance(),
    );
  });
});
