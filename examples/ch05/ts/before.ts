// BEFORE: a train wreck and ask-then-decide, in one line.
//
// freeShipping reaches through customer -> membership -> tier (content
// coupling: it now depends on the shape of three classes), then pulls the
// order's subtotal out to make a decision the order could make itself.

export const FREE_SHIPPING_MIN = 100;

export interface Membership {
  readonly tier: "standard" | "gold";
}

export interface Customer {
  readonly name: string;
  readonly email: string;
  readonly membership: Membership;
}

export interface LineItem {
  readonly name: string;
  readonly price: number;
}

export interface Order {
  readonly customer: Customer;
  readonly items: readonly LineItem[];
  readonly country: string;
  readonly giftWrap: boolean;
}

export const subtotal = (order: Order): number =>
  order.items.reduce((sum, item) => sum + item.price, 0);

export function freeShipping(order: Order): boolean {
  // talks to strangers (customer.membership.tier) and asks-then-decides
  return order.customer.membership.tier === "gold" && subtotal(order) >= FREE_SHIPPING_MIN;
}
