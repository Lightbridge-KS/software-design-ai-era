// Factory — canonical conceptual example. Run: npx tsx conceptFactory.ts
//
// The classical Factory Method shape: a Creator declares a factory method that
// returns a Product; subclasses decide the concrete Product. Read this as the
// structure the *name* denotes — then see the idiomatic registry form below,
// which is what you will usually write.

// --- Canonical: Factory Method (a hierarchy decides its product) -------------

export interface Product {
  operation(): string;
}

export class ConcreteProductA implements Product {
  operation(): string {
    return "result-A";
  }
}

export class ConcreteProductB implements Product {
  operation(): string {
    return "result-B";
  }
}

export abstract class Creator {
  // Subclasses choose the concrete Product; the base stays independent.
  protected abstract factoryMethod(): Product;

  operation(): string {
    const product = this.factoryMethod(); // uses the product without naming its type
    return `Creator works with ${product.operation()}`;
  }
}

export class CreatorA extends Creator {
  protected factoryMethod(): Product {
    return new ConcreteProductA();
  }
}

export class CreatorB extends Creator {
  protected factoryMethod(): Product {
    return new ConcreteProductB();
  }
}

// --- Idiomatic: a record of constructor thunks IS the factory ---------------

export const PRODUCTS: Record<string, () => Product> = {
  a: () => new ConcreteProductA(),
  b: () => new ConcreteProductB(),
};

export function makeProduct(kind: string): Product {
  const build = PRODUCTS[kind];
  if (build === undefined) {
    throw new Error(`unknown product: ${kind}`);
  }
  return build();
}

// Demo
console.log(new CreatorA().operation()); // Creator works with result-A
console.log(makeProduct("b").operation()); // result-B
