// AFTER: ask one object one question.
//
// Each object answers for what it owns, talking only to immediate friends.
// The caller knows nothing about membership or tiers — so when that graph is
// remodeled, the caller doesn't move. Fields are `readonly`; the decisions are
// getters, so callers ask without paying a method call's ceremony.

export const FREE_SHIPPING_MIN = 100;

export class Membership {
  constructor(readonly tier: "standard" | "gold") {}

  get isGold(): boolean {
    return this.tier === "gold";
  }
}

export class Customer {
  constructor(
    readonly name: string,
    readonly email: string,
    readonly membership: Membership,
  ) {}

  get isVip(): boolean {
    return this.membership.isGold; // one hop, to an immediate friend
  }
}

export interface LineItem {
  readonly name: string;
  readonly price: number;
}

export class Order {
  constructor(
    readonly customer: Customer,
    readonly items: readonly LineItem[],
    readonly country: string = "US",
    readonly giftWrap: boolean = false,
  ) {}

  get subtotal(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }

  get qualifiesForFreeShipping(): boolean {
    return this.customer.isVip && this.subtotal >= FREE_SHIPPING_MIN;
  }
}

export function freeShipping(order: Order): boolean {
  return order.qualifiesForFreeShipping; // knows nothing of the customer graph
}
