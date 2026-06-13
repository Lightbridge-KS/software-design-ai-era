// Chapter 6 · BEFORE: a cart that cannot protect itself.
//
// Everything is a public mutable field, so nothing is safe. `total` is a plain
// number the caller must remember to recompute (they won't), and `discountRate`
// accepts any number at all. The object has no way to keep its own promises.

import { type LineItem } from "./models";

export class ShoppingCart {
  items: LineItem[] = [];
  discountRate = 0; // no guard: 2.0 (200% off) is accepted without complaint
  total = 0; // a cached field the caller must keep in sync by hand

  recompute(): void {
    const subtotal = this.items.reduce((sum, item) => sum + item.price, 0);
    this.total = Math.round(subtotal * (1 - this.discountRate) * 100) / 100;
  }
}
