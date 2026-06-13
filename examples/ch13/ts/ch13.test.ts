// Chapter 13 tests — the design's claims, executable. Mirrors the Python suite:
// each rule is testable alone, and the refactored forms match the tangle's behavior.

import { describe, expect, it } from "vitest";
import { type Order } from "./models";
import * as before from "./before";
import * as classical from "./afterClassical";
import * as idiomatic from "./afterIdiomatic";

const order: Order = {
  items: [
    { name: "coffee", price: 12.5 },
    { name: "mug", price: 7.5 },
  ],
  isMember: false,
};

const memberOrder: Order = {
  items: [{ name: "coffee", price: 20 }],
  isMember: true,
};

const KINDS = ["none", "tenPercent", "coupon5", "member"] as const;

const classicalRules: Record<string, classical.DiscountRule> = {
  none: new classical.NoDiscount(),
  tenPercent: new classical.PercentageOff(0.1),
  coupon5: new classical.CouponOff(5),
  member: new classical.MemberDiscount(),
};

describe("Strategy: refactored forms preserve the tangle's behavior", () => {
  it.each(KINDS)("classical matches before for %s", (kind) => {
    expect(classical.applyDiscount(order, classicalRules[kind]!)).toBe(
      before.applyDiscount(order, kind),
    );
  });

  it.each(KINDS)("idiomatic matches before for %s", (kind) => {
    expect(idiomatic.applyDiscount(order, idiomatic.RULES[kind]!)).toBe(
      before.applyDiscount(order, kind),
    );
  });
});

describe("Strategy: each rule is testable alone, no dispatch in the way", () => {
  it("member rule alone", () => {
    expect(idiomatic.memberDiscount(memberOrder)).toBe(17);
  });

  it("member rule ignores non-members", () => {
    expect(idiomatic.memberDiscount(order)).toBe(20);
  });

  it("coupon never goes negative", () => {
    const small: Order = { items: [{ name: "sticker", price: 2 }], isMember: false };
    expect(idiomatic.couponOff(5)(small)).toBe(0);
  });
});

describe("Template Method: skeleton fixed, output identical to the tangle", () => {
  it("text receipt matches before", () => {
    expect(new classical.PlainTextReceipt().render(order)).toBe(
      before.renderTextReceipt(order),
    );
  });

  it("html receipt matches before", () => {
    expect(new classical.HtmlReceipt().render(order)).toBe(
      before.renderHtmlReceipt(order),
    );
  });

  it("skeleton owns the step order", () => {
    const text = new classical.PlainTextReceipt().render(order);
    expect(text.indexOf("RECEIPT")).toBeLessThan(text.indexOf("coffee"));
    expect(text.indexOf("coffee")).toBeLessThan(text.indexOf("Total:"));
  });
});
