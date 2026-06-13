// Shared checkout-lite model. Real money wants integer cents; number keeps these
// teaching examples short. LineItem and Order are plain readonly data (structural
// types); `subtotal` is a free function rather than a method.

export interface LineItem {
  readonly name: string;
  readonly price: number;
}

export interface Order {
  readonly items: readonly LineItem[];
  readonly isMember: boolean;
}

export const subtotal = (order: Order): number =>
  order.items.reduce((sum, item) => sum + item.price, 0);
