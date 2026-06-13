// Chapter 9 · BEFORE: the cathedral.
//
// A few hundred lines (in spirit) answering a thirty-line question: "save
// completed orders to disk so we can reload them later."
//
// Every piece is individually defensible. The sum is not. Each class below is
// annotated with the future it speculates about — none of which was requested.

import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { type LineItem, type Order } from "./models";

// Speculates: paths will need environment-based configuration someday.
export interface StorageSettings {
  readonly storageDir: string;
  readonly filename: string;
}

export function storageSettingsFromEnv(): StorageSettings {
  return {
    storageDir: process.env.ORDERS_STORAGE_DIR ?? ".",
    filename: process.env.ORDERS_FILENAME ?? "orders.json",
  };
}

// Speculates: line-item serialization will vary someday.
export class LineItemSerializer {
  toJSON(item: LineItem): Record<string, unknown> {
    return { name: item.name, price: item.price };
  }

  fromJSON(data: Record<string, unknown>): LineItem {
    return { name: String(data.name), price: Number(data.price) };
  }
}

// Speculates: order serialization will vary someday.
export class OrderSerializer {
  private readonly itemSerializer = new LineItemSerializer();

  toJSON(order: Order): Record<string, unknown> {
    return {
      items: order.items.map((i) => this.itemSerializer.toJSON(i)),
      isMember: order.isMember,
    };
  }

  fromJSON(data: Record<string, unknown>): Order {
    const items = (data.items as Record<string, unknown>[]).map((d) =>
      this.itemSerializer.fromJSON(d),
    );
    return { items, isMember: Boolean(data.isMember) };
  }
}

// Speculates: a second storage backend someday.
export interface IOrderRepository {
  save(orders: readonly Order[]): void;
  load(): Order[];
}

// The interface's only implementation — and no second in sight.
export class JsonOrderRepository implements IOrderRepository {
  private readonly path: string;
  private readonly serializer = new OrderSerializer();

  constructor(settings: StorageSettings) {
    this.path = join(settings.storageDir, settings.filename);
  }

  save(orders: readonly Order[]): void {
    const payload = orders.map((o) => this.serializer.toJSON(o));
    writeFileSync(this.path, JSON.stringify(payload, null, 2));
  }

  load(): Order[] {
    const payload = JSON.parse(readFileSync(this.path, "utf-8")) as Record<
      string,
      unknown
    >[];
    return payload.map((d) => this.serializer.fromJSON(d));
  }
}

// A factory that can only ever produce one type.
export class OrderRepositoryFactory {
  static create(kind = "json"): IOrderRepository {
    if (kind === "json") {
      return new JsonOrderRepository(storageSettingsFromEnv());
    }
    throw new Error(`unknown repository kind: ${kind}`);
  }
}
