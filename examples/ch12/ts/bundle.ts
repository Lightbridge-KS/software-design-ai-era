// Chapter 12 · Composite: treat a tree of line items uniformly.
//
// Product is a leaf; Bundle is a composite holding other line items (products
// or sub-bundles). Both satisfy LineItem, so a cart totals itself with no type
// checks and no special-casing of branches versus leaves.

export interface LineItem {
  price(): number;
}

export class Product implements LineItem {
  constructor(
    readonly name: string,
    private readonly amount: number,
  ) {}
  price(): number {
    return this.amount;
  }
}

export class Bundle implements LineItem {
  private readonly items: LineItem[];
  constructor(
    readonly name: string,
    items: LineItem[] = [],
  ) {
    this.items = [...items];
  }
  add(item: LineItem): void {
    this.items.push(item);
  }
  price(): number {
    return this.items.reduce((sum, item) => sum + item.price(), 0); // recurse
  }
}

export const cartTotal = (items: readonly LineItem[]): number =>
  items.reduce((sum, item) => sum + item.price(), 0); // leaf and branch alike
