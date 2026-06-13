// Pricing — answers to one actor: finance/commerce rules. One reason to change:
// the money math. No I/O, no email, no disk — which is exactly why it is testable
// in isolation.

import { type Order, subtotal } from "./models";

const TAX_RATES: Record<string, number> = { US: 0.07, DE: 0.19, JP: 0.1 };
const EU_COUNTRIES = ["DE", "FR", "NL"];

export const memberDiscount = (sub: number, isMember: boolean): number =>
  isMember ? sub * 0.85 : sub;

export const taxFor = (amount: number, country: string): number =>
  amount * (TAX_RATES[country] ?? 0);

export const shippingFor = (country: string, giftWrap: boolean): number => {
  let base: number;
  if (country === "US") {
    base = 5.0;
  } else if (EU_COUNTRIES.includes(country)) {
    base = 9.9;
  } else {
    base = 24.9;
  }
  return base + (giftWrap ? 3.5 : 0);
};

export const orderTotal = (order: Order): number => {
  const discounted = memberDiscount(subtotal(order), order.customer.isMember);
  const tax = taxFor(discounted, order.country);
  const shipping = shippingFor(order.country, order.giftWrap);
  return Math.round((discounted + tax + shipping) * 100) / 100;
};
