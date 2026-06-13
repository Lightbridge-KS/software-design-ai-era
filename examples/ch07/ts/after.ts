// Chapter 7 · AFTER: the promise written down and enforced.
//
// Two complementary forms:
//   - applyPercentageDiscount: states its contract and fails fast on bad input
//     at the boundary with a thrown Error that names its cause.
//   - Percent + discount: "parse, don't validate" — a raw number becomes a
//     proven Percent once, and downstream code trusts it without re-checking.

const round2 = (value: number): number => Math.round(value * 100) / 100;

/**
 * Return `price` reduced by `percent` percent.
 *
 * Precondition:  0 <= percent <= 100 (checked at runtime; the type is widened).
 * Postcondition: result is non-negative and rounded to cents.
 */
export function applyPercentageDiscount(price: number, percent: number): number {
  if (!(percent >= 0 && percent <= 100)) {
    throw new RangeError(`percent must be in [0, 100], got ${percent}`);
  }
  return round2(price * (1 - percent / 100));
}

// "Parse, don't validate." Percent is a branded type: a plain number that the
// compiler will not accept as a Percent until it has passed through `percent()`.
// Once a value is typed Percent, it is guaranteed valid — downstream code that
// receives a Percent never re-checks, because an invalid one cannot be made.
declare const percentBrand: unique symbol;
export type Percent = number & { readonly [percentBrand]: true };

/** The sole parser: a raw number in, a proven Percent out (or it throws). */
export function percent(value: number): Percent {
  if (!(value >= 0 && value <= 100)) {
    throw new RangeError(`percent must be in [0, 100], got ${value}`);
  }
  return value as Percent;
}

/** Takes an already-parsed Percent — the validity is guaranteed by its type. */
export function discount(price: number, pct: Percent): number {
  return round2(price * (1 - pct / 100));
}

// At a real boundary the input arrives as `unknown` (JSON, a form field, an env
// var). Narrow it, then parse it — after this, the rest of the program holds a
// Percent and forgets the raw value ever existed.
export function parsePercentFromInput(raw: unknown): Percent {
  if (typeof raw !== "number") {
    throw new TypeError(`percent must be a number, got ${typeof raw}`);
  }
  return percent(raw);
}
