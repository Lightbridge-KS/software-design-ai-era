// Chapter 9 · AFTER: right-sized.
//
// Same behavior as the cathedral; roughly eighty percent less code. The `path`
// parameter is the flexibility the settings system promised — a function
// argument is the cheapest seam there is.

import { readFileSync, writeFileSync } from "node:fs";
import { type LineItem, type Order } from "./models";

export function saveOrders(orders: readonly Order[], path: string): void {
  const payload = orders.map((o) => ({
    items: o.items.map((i) => ({ name: i.name, price: i.price })),
    isMember: o.isMember,
  }));
  writeFileSync(path, JSON.stringify(payload, null, 2));
}

export function loadOrders(path: string): Order[] {
  const payload = JSON.parse(readFileSync(path, "utf-8")) as {
    items: LineItem[];
    isMember: boolean;
  }[];
  return payload.map((entry) => ({
    items: entry.items.map((item) => ({ name: item.name, price: item.price })),
    isMember: entry.isMember,
  }));
}
