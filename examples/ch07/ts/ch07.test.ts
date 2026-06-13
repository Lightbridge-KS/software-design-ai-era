// Chapter 7 tests — contracts made executable. Mirrors the Python suite.
//
// The before tests demonstrate the surprises an uncontracted function allows.
// The after tests prove the promise is kept: bad input fails fast at the
// boundary, and an invalid Percent cannot be constructed at all.

import { describe, expect, it } from "vitest";
import * as before from "./before";
import * as after from "./after";

// --- BEFORE: the function astonishes ----------------------------------------

describe("before: the uncontracted function astonishes", () => {
  it("silently confuses units (0.2 meant as 20% -> a 0.2% discount)", () => {
    expect(before.applyDiscount(100, 0.2)).toBeCloseTo(99.8, 10);
  });

  it("allows a negative price (150% off) without complaint", () => {
    expect(before.applyDiscount(100, 150)).toBe(-50);
  });
});

// --- AFTER: the contract is kept --------------------------------------------

describe("after: the contract is kept", () => {
  it("computes the correct discount", () => {
    expect(after.applyPercentageDiscount(100, 20)).toBe(80);
  });

  it.each([150, -5])("fails fast at the boundary for %d", (bad) => {
    expect(() => after.applyPercentageDiscount(100, bad)).toThrow();
  });

  it("the error names its cause (mentions 'percent')", () => {
    expect(() => after.applyPercentageDiscount(100, 150)).toThrow(/percent/);
  });

  it.each([
    [100, 20, 80],
    [10, 0, 10],
    [10, 100, 0],
  ])("postcondition holds: discount(%d, %d) == %d, non-negative, rounded", (price, pct, expected) => {
    const result = after.applyPercentageDiscount(price, pct);
    expect(result).toBe(expected);
    expect(result).toBeGreaterThanOrEqual(0);
    expect(result).toBe(Math.round(result * 100) / 100);
  });
});

// --- PARSE, DON'T VALIDATE: an invalid Percent cannot exist -----------------

describe("parse, don't validate: an invalid Percent cannot be made", () => {
  it.each([150, -1])("the parser throws on out-of-range input %d", (bad) => {
    expect(() => after.percent(bad)).toThrow(/percent/);
  });

  it("downstream trusts the parsed type without re-checking", () => {
    // discount() does no validation; it relies on Percent having been parsed.
    expect(after.discount(100, after.percent(20))).toBe(80);
  });

  it("rejects a non-number at an unknown-typed boundary", () => {
    expect(() => after.parsePercentFromInput("20")).toThrow();
    // a parsed boundary value flows on as a proven Percent
    expect(after.discount(100, after.parsePercentFromInput(20))).toBe(80);
  });
});
