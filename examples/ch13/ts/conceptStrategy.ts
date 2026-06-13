// Strategy — canonical conceptual example. Run: npx tsx conceptStrategy.ts
//
// Encapsulate interchangeable algorithms behind a common interface and inject the
// chosen one. The canonical class form is what the name denotes; in TS a strategy
// is usually just a function in a record.

// --- Canonical: a Strategy interface, injected into a Context ----------------

export interface Strategy {
  execute(data: number[]): number[];
}

export class AscendingStrategy implements Strategy {
  execute(data: number[]): number[] {
    return [...data].sort((a, b) => a - b);
  }
}

export class DescendingStrategy implements Strategy {
  execute(data: number[]): number[] {
    return [...data].sort((a, b) => b - a);
  }
}

export class Context {
  constructor(private readonly strategy: Strategy) {}
  doWork(data: number[]): number[] {
    return this.strategy.execute(data); // delegates to the injected strategy
  }
}

// --- Idiomatic: a strategy is a function; a record selects one --------------

export type SortStrategy = (data: number[]) => number[];

export const STRATEGIES: Record<string, SortStrategy> = {
  asc: (d) => [...d].sort((a, b) => a - b),
  desc: (d) => [...d].sort((a, b) => b - a),
};

// Demo
console.log(new Context(new DescendingStrategy()).doWork([3, 1, 2])); // [3, 2, 1]
console.log(STRATEGIES.asc?.([3, 1, 2])); // [1, 2, 3]
