// AFTER, idiomatic form. A strategy is just a function. The RULES record is the
// registry — the single place where "which rules exist" is recorded.

import { type Order, subtotal } from "./models";

export type DiscountRule = (order: Order) => number;

export const noDiscount: DiscountRule = (order) => subtotal(order);

// A closure carries configuration the way a constructor would, without a class:
export const percentageOff =
  (rate: number): DiscountRule =>
  (order) =>
    subtotal(order) * (1 - rate);

export const couponOff =
  (amount: number): DiscountRule =>
  (order) =>
    Math.max(subtotal(order) - amount, 0);

export const memberDiscount: DiscountRule = (order) =>
  order.isMember ? subtotal(order) * 0.85 : subtotal(order);

export const RULES: Record<string, DiscountRule> = {
  none: noDiscount,
  tenPercent: percentageOff(0.1),
  coupon5: couponOff(5),
  member: memberDiscount,
};

export function applyDiscount(order: Order, rule: DiscountRule): number {
  return rule(order);
}
