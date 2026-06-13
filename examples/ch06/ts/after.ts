// Chapter 6 · AFTER: a cart that keeps its own promises.
//
// A narrow public surface over a hidden implementation. `#items` and
// `#discountRate` are truly private (no caller can reach them). `total` is a
// computed getter, so it can never go stale or lie; `discountRate` validates on
// the way in; `items` returns a readonly view. There is no way to put this cart
// into an illegal state from the outside.

import { type LineItem } from "./models";

export class ShoppingCart {
  #items: LineItem[] = [];
  #discountRate = 0;

  addItem(item: LineItem): void {
    this.#items.push(item);
  }

  get items(): readonly LineItem[] {
    return [...this.#items]; // a readonly copy; mutating it can't corrupt us
  }

  get discountRate(): number {
    return this.#discountRate;
  }

  set discountRate(rate: number) {
    if (rate < 0 || rate > 1) {
      throw new RangeError(`discountRate must be in [0, 1], got ${rate}`);
    }
    this.#discountRate = rate;
  }

  get total(): number {
    // Computed on read — never stale. No setter, so the lie is unrepresentable.
    const subtotal = this.#items.reduce((sum, item) => sum + item.price, 0);
    return Math.round(subtotal * (1 - this.#discountRate) * 100) / 100;
  }
}
