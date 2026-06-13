// Chapter 15 tests — Iterator and Visitor, made executable. Mirrors the Python suite.
//
// Iterator: a catalog iterates without exposing its array, and a generator
// streams batches. Visitor: two operations walk the same Chapter-12 tree, and
// the discriminated-union switch agrees with the classical visitor.

import { describe, expect, it } from "vitest";
import { Catalog, paged, type Product } from "./catalog";
import {
  Bundle,
  CountItemsVisitor,
  Product as LineProduct,
  TotalPriceVisitor,
  totalViaSwitch,
  type Node,
} from "./visitor";

// --- Iterator ---------------------------------------------------------------

describe("Iterator: traverse without exposing the container", () => {
  it("a catalog is iterable with a for-of loop", () => {
    const catalog = new Catalog([
      { name: "mug", price: 12 },
      { name: "pen", price: 3 },
    ]);
    const names = [...catalog].map((p) => p.name);
    expect(names).toEqual(["mug", "pen"]);
    expect(catalog.size).toBe(2);
  });

  it("paged streams fixed-size batches lazily", () => {
    const products: Product[] = Array.from({ length: 5 }, (_, i) => ({
      name: String(i),
      price: i,
    }));
    const batches = [...paged(products, 2)];
    expect(batches.map((b) => b.length)).toEqual([2, 2, 1]);
  });
});

// --- Visitor ----------------------------------------------------------------

describe("Visitor: operations over the Chapter 12 tree", () => {
  const tree = (): Bundle =>
    new Bundle("kit", [
      new LineProduct("mug", 12),
      new Bundle("duo", [new LineProduct("light", 9), new LineProduct("dark", 9)]),
    ]);

  it("totals the tree via double dispatch", () => {
    expect(tree().accept(new TotalPriceVisitor())).toBe(30);
  });

  it("counts items by reusing the same tree", () => {
    expect(tree().accept(new CountItemsVisitor())).toBe(3);
  });

  it("the discriminated-union switch agrees with the visitor", () => {
    const node: Node = {
      kind: "bundle",
      items: [
        { kind: "product", price: 12 },
        {
          kind: "bundle",
          items: [
            { kind: "product", price: 9 },
            { kind: "product", price: 9 },
          ],
        },
      ],
    };
    expect(totalViaSwitch(node)).toBe(30);
  });
});
