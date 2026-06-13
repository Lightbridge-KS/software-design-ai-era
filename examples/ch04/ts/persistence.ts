// Persistence — answers to one actor: engineering (how orders are stored). One
// reason to change: the storage format. Move to a database and only this module
// changes.

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { type Order } from "./models";

interface OrderRecord {
  readonly customer: string;
  readonly total: number;
}

export const saveOrder = (
  order: Order,
  total: number,
  ordersFile = "orders.json",
): void => {
  const record: OrderRecord = { customer: order.customer.name, total };
  const existing: OrderRecord[] = existsSync(ordersFile)
    ? (JSON.parse(readFileSync(ordersFile, "utf8")) as OrderRecord[])
    : [];
  existing.push(record);
  writeFileSync(ordersFile, JSON.stringify(existing, null, 2));
};
