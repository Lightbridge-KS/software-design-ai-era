// checkout-lite domain model (shared by before and after). Plain readonly data
// (structural types); `subtotal` is a free function rather than a method. Real
// money wants integer cents; number keeps these teaching examples short.

export interface LineItem {
  readonly name: string;
  readonly price: number;
}

export interface Customer {
  readonly name: string;
  readonly email: string;
  readonly isMember: boolean;
}

export interface Order {
  readonly customer: Customer;
  readonly items: readonly LineItem[];
  readonly country: string;
  readonly giftWrap: boolean;
}

export const subtotal = (order: Order): number =>
  order.items.reduce((sum, item) => sum + item.price, 0);
