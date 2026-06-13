// Chapter 9 tests — the same behavioral contract, run against both designs.
// Mirrors the Python suite: the cathedral and the two functions are behaviorally
// identical, and the simple form is far smaller. Everything the cathedral adds is
// structure the contract never asked for.

import { describe, expect, it } from "vitest";
import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { type Order } from "./models";
import * as before from "./before";
import * as after from "./after";

const ORDERS: Order[] = [
  { items: [{ name: "coffee", price: 12.5 }, { name: "mug", price: 7.5 }], isMember: false },
  { items: [{ name: "beans", price: 18.0 }], isMember: true },
  { items: [], isMember: false }, // empty order: the edge case both designs must honor
];

function tmpFile(name: string): string {
  return join(mkdtempSync(join(tmpdir(), "ch09-")), name);
}

function cathedralRoundtrip(orders: readonly Order[], path: string): Order[] {
  const dir = path.slice(0, path.lastIndexOf("/"));
  const filename = path.slice(path.lastIndexOf("/") + 1);
  const repo = new before.JsonOrderRepository({ storageDir: dir, filename });
  repo.save(orders);
  return repo.load();
}

function simpleRoundtrip(orders: readonly Order[], path: string): Order[] {
  after.saveOrders(orders, path);
  return after.loadOrders(path);
}

const roundtrips: Record<string, (o: readonly Order[], p: string) => Order[]> = {
  cathedral: cathedralRoundtrip,
  simple: simpleRoundtrip,
};

describe("both designs satisfy the same behavioral contract", () => {
  it.each(Object.keys(roundtrips))("%s roundtrip preserves orders", (name) => {
    const path = tmpFile("orders.json");
    expect(roundtrips[name]!(ORDERS, path)).toEqual(ORDERS);
  });

  it("both designs write byte-identical files", () => {
    const cathedralPath = tmpFile("cathedral.json");
    const simplePath = tmpFile("simple.json");
    cathedralRoundtrip(ORDERS, cathedralPath);
    simpleRoundtrip(ORDERS, simplePath);
    expect(readFileSync(simplePath, "utf-8")).toBe(readFileSync(cathedralPath, "utf-8"));
  });

  it("the factory produces its one and only type", () => {
    const repo = before.OrderRepositoryFactory.create();
    expect(repo).toBeInstanceOf(before.JsonOrderRepository);
  });
});

describe("the deletion is the lesson: simple is far smaller", () => {
  it("after.ts is well under half the size of before.ts", () => {
    const here = new URL(".", import.meta.url).pathname;
    const beforeLoc = readFileSync(join(here, "before.ts"), "utf-8").split("\n").length;
    const afterLoc = readFileSync(join(here, "after.ts"), "utf-8").split("\n").length;
    expect(afterLoc).toBeLessThan(beforeLoc / 2);
  });
});
