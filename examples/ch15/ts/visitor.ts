// Chapter 15 · Visitor: add operations over a node tree without editing nodes.
//
// The line-item tree from Chapter 12 (Product leaf, Bundle composite). A visitor
// carries one operation across node types via double dispatch. The idiomatic TS
// replacement is a discriminated union + exhaustive switch (totalViaSwitch).

export interface LineItemVisitor<T> {
  visitProduct(product: Product): T;
  visitBundle(bundle: Bundle): T;
}

export interface LineItem {
  accept<T>(visitor: LineItemVisitor<T>): T;
}

export class Product implements LineItem {
  constructor(
    readonly name: string,
    readonly price: number,
  ) {}
  accept<T>(visitor: LineItemVisitor<T>): T {
    return visitor.visitProduct(this); // dispatch to the product branch
  }
}

export class Bundle implements LineItem {
  constructor(
    readonly name: string,
    readonly items: LineItem[] = [],
  ) {}
  accept<T>(visitor: LineItemVisitor<T>): T {
    return visitor.visitBundle(this); // dispatch to the bundle branch
  }
}

export class TotalPriceVisitor implements LineItemVisitor<number> {
  visitProduct(product: Product): number {
    return product.price;
  }
  visitBundle(bundle: Bundle): number {
    return bundle.items.reduce((sum, item) => sum + item.accept(this), 0);
  }
}

export class CountItemsVisitor implements LineItemVisitor<number> {
  visitProduct(_product: Product): number {
    return 1;
  }
  visitBundle(bundle: Bundle): number {
    return bundle.items.reduce((sum, item) => sum + item.accept(this), 0);
  }
}

// --- Idiomatic replacement: discriminated union + exhaustive switch ----------

export type Node =
  | { readonly kind: "product"; readonly price: number }
  | { readonly kind: "bundle"; readonly items: readonly Node[] };

export const totalViaSwitch = (node: Node): number => {
  switch (node.kind) {
    case "product":
      return node.price;
    case "bundle":
      return node.items.reduce((sum, child) => sum + totalViaSwitch(child), 0);
    default: {
      const _exhaustive: never = node; // compile error if a case is ever missed
      return _exhaustive;
    }
  }
};
