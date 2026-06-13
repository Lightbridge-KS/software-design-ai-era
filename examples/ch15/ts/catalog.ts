// Chapter 15 · Iterator: traverse without exposing the container.
//
// Catalog is iterable (`for (const p of catalog)`) without leaking its internal
// array. paged() is a generator: it streams fixed-size batches lazily.

export interface Product {
  readonly name: string;
  readonly price: number;
}

export class Catalog implements Iterable<Product> {
  constructor(private readonly products: Product[]) {}
  [Symbol.iterator](): Iterator<Product> {
    return this.products[Symbol.iterator](); // delegate to the array's iterator
  }
  get size(): number {
    return this.products.length;
  }
}

export function* paged(products: Product[], size: number): Generator<Product[]> {
  for (let start = 0; start < products.length; start += size) {
    yield products.slice(start, start + size); // yield batches lazily
  }
}
