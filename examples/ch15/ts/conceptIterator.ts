// Iterator — canonical conceptual example. Run: npx tsx conceptIterator.ts
//
// The classical form implements [Symbol.iterator]/next. The idiomatic form is a
// generator — the same protocol, written with function* and yield.

export class CountUp implements Iterable<number> {
  constructor(private readonly limit: number) {}
  [Symbol.iterator](): Iterator<number> {
    let n = 0;
    const limit = this.limit;
    return {
      next(): IteratorResult<number> {
        if (n >= limit) return { done: true, value: undefined };
        n += 1;
        return { done: false, value: n };
      },
    };
  }
}

export function* countUp(limit: number): Generator<number> {
  for (let n = 1; n <= limit; n++) yield n;
}

// Demo
console.log([...new CountUp(3)]); // [1, 2, 3]
console.log([...countUp(3)]); // [1, 2, 3]
