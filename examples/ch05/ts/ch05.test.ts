// Chapter 5 tests — coupling made executable. Mirrors the Python suite.
//
// Three claims:
//   1. The refactor preserved behavior (before === after).
//   2. The caller has Least Knowledge: the after's freeShipping never mentions
//      'membership' or 'tier' — so remodeling that graph won't touch it.
//   3. Dependency direction: the domain model imports nothing volatile (no I/O).

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import * as before from "./before";
import * as after from "./after";

type Tier = "standard" | "gold";

// (tier, subtotal, expected free shipping)
const CASES: ReadonlyArray<readonly [Tier, number, boolean]> = [
  ["gold", 150, true],
  ["gold", 50, false], // VIP, but under the threshold
  ["standard", 150, false],
  ["standard", 50, false],
];

const makeBefore = (tier: Tier, price: number): before.Order => ({
  customer: {
    name: "Sam",
    email: "s@x.com",
    membership: { tier },
  },
  items: [{ name: "a", price }],
  country: "US",
  giftWrap: false,
});

const makeAfter = (tier: Tier, price: number): after.Order =>
  new after.Order(
    new after.Customer("Sam", "s@x.com", new after.Membership(tier)),
    [{ name: "a", price }],
  );

describe("Least Knowledge: the refactor preserved behavior", () => {
  it.each(CASES)("tier=%s price=%d -> %s", (tier, price, expected) => {
    const b = before.freeShipping(makeBefore(tier, price));
    const a = after.freeShipping(makeAfter(tier, price));
    expect(b).toBe(expected);
    expect(a).toBe(expected);
  });
});

describe("Least Knowledge: the caller knows no graph shape", () => {
  it("after's freeShipping mentions neither 'membership' nor 'tier'", () => {
    // The structural claim, in TS: read the source and assert the caller's body
    // is innocent of the customer graph. Remodel tiers and this function is safe.
    const src = readFileSync(fileURLToPath(new URL("./after.ts", import.meta.url)), "utf8");
    const body = src.split("export function freeShipping")[1]!;
    expect(body).not.toContain("membership");
    expect(body).not.toContain("tier");
  });
});

describe("Dependency direction: the stable model depends on nothing volatile", () => {
  it("after imports no I/O", () => {
    const src = readFileSync(fileURLToPath(new URL("./after.ts", import.meta.url)), "utf8");
    for (const volatileMod of ["node:fs", "node:net", "nodemailer", "node:http"]) {
      expect(src).not.toContain(volatileMod);
    }
  });
});
