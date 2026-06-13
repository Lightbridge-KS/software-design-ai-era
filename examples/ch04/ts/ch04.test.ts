// Chapter 4 tests — the split preserves behavior, and unlocks isolation. Mirrors the
// Python suite's claims:
//   1. Splitting by responsibility changed no observable behavior (before == after).
//   2. The cohesion payoff: pricing is now testable with NO email transport and NO
//      filesystem, because it no longer depends on them.

import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { type Customer, type LineItem, type Order } from "./models";
import { checkout as after } from "./checkout";
import { checkout as before } from "./before";
import { orderTotal } from "./pricing";

const customer = (name: string, isMember = false): Customer => ({
  name,
  email: `${name.toLowerCase()}@x.com`,
  isMember,
});

const order = (c: Customer, price: number, country: string, giftWrap = false): Order => ({
  customer: c,
  items: [{ name: "a", price } satisfies LineItem],
  country,
  giftWrap,
});

const CASES: readonly Order[] = [
  order(customer("Sam"), 100, "US"),
  order(customer("Mia", true), 100, "US"),
  order(customer("Lena"), 80, "DE", true),
  order(customer("Ken", true), 50, "JP"),
  order(customer("Ana"), 30, "CA"), // no tax
];

// Each run gets its own temp files so before/after never share state and the suite
// touches no fixed path on disk.
const tmpFiles = (): { ordersFile: string; outboxFile: string } => {
  const dir = mkdtempSync(join(tmpdir(), "ch04-"));
  return { ordersFile: join(dir, "orders.json"), outboxFile: join(dir, "outbox.txt") };
};

describe("the split preserves behavior", () => {
  it.each(CASES)("after matches before for %o", (o) => {
    const a = tmpFiles();
    const b = tmpFiles();
    expect(after(o, "tok", false, a.ordersFile, a.outboxFile)).toBe(
      before(o, "tok", false, b.ordersFile, b.outboxFile),
    );
  });
});

describe("the cohesion payoff: pricing is pure, no I/O needed", () => {
  it.each(CASES)("orderTotal is a rounded number for %o", (o) => {
    const total = orderTotal(o);
    expect(typeof total).toBe("number");
    expect(total).toBe(Math.round(total * 100) / 100);
  });

  it("member pricing is discounted before tax — verifiable without any I/O", () => {
    const member = order(customer("Mia", true), 100, "US");
    // 100 * 0.85 = 85; +7% = 90.95; +5.00 = 95.95
    expect(orderTotal(member)).toBe(95.95);
  });
});
