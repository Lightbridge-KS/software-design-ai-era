// Chapter 12 tests — Composite and Decorator, made executable. Mirrors Python.
//
// Composite: leaf and bundle answer price() uniformly, and a bundle recurses
// into a nested bundle. Decorator: behavior wraps the gateway without editing
// it, and decorators stack at runtime while preserving the interface.

import { describe, expect, it } from "vitest";
import { Bundle, Product, cartTotal, type LineItem } from "./bundle";
import {
  LoggingGateway,
  RetryingGateway,
  StripeGateway,
  TransientError,
  type IPaymentGateway,
  type Receipt,
} from "./gatewayDecorators";

// --- Composite --------------------------------------------------------------

describe("Composite: leaf and bundle are treated uniformly", () => {
  it("a bundle prices itself by recursing into children", () => {
    const kit = new Bundle("starter-kit", [
      new Product("mug", 12),
      new Bundle("beans-duo", [new Product("light", 9), new Product("dark", 9)]),
    ]);
    expect(kit.price()).toBe(30); // 12 + (9 + 9) — one real nested level
  });

  it("a cart totals leaves and bundles with no type checks", () => {
    const items: LineItem[] = [
      new Product("mug", 12),
      new Bundle("duo", [new Product("a", 3), new Product("b", 4)]),
    ];
    expect(cartTotal(items)).toBe(19);
  });
});

// --- Decorator --------------------------------------------------------------

describe("Decorator: behavior stacks without editing the gateway", () => {
  it("logging records around the delegated charge", () => {
    const log: string[] = [];
    const gateway: IPaymentGateway = new LoggingGateway(new StripeGateway(), log);
    const receipt: Receipt = gateway.charge(10);
    expect(receipt.confirmation).toBe("ch_1000");
    expect(log).toEqual(["charging 10.00", "charged ch_1000"]);
  });

  it("retry recovers from transient failures, preserving the interface", () => {
    let calls = 0;
    const flaky: IPaymentGateway = {
      charge(amount: number): Receipt {
        calls++;
        if (calls < 3) throw new TransientError("try again");
        return { provider: "flaky", amount, confirmation: "ok" };
      },
    };
    const gateway = new RetryingGateway(flaky, 2);
    expect(gateway.charge(5).confirmation).toBe("ok");
    expect(calls).toBe(3);
  });

  it("stacks at runtime: retry wraps logging wraps stripe", () => {
    const log: string[] = [];
    const gateway = new RetryingGateway(new LoggingGateway(new StripeGateway(), log));
    expect(gateway.charge(20).confirmation).toBe("ch_2000");
    expect(log).toEqual(["charging 20.00", "charged ch_2000"]);
  });
});
