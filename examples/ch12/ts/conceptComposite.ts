// Composite — canonical conceptual example. Run: npx tsx conceptComposite.ts
//
// A Component interface; a Leaf implements it directly; a Composite holds
// children (each itself a Component) and aggregates their results. The client
// treats leaf and composite identically.

export interface Component {
  operation(): number;
}

export class Leaf implements Component {
  constructor(private readonly value: number) {}
  operation(): number {
    return this.value;
  }
}

export class Composite implements Component {
  private readonly children: Component[] = [];
  add(child: Component): void {
    this.children.push(child);
  }
  operation(): number {
    return this.children.reduce((sum, c) => sum + c.operation(), 0); // aggregate
  }
}

// Demo
const root = new Composite();
root.add(new Leaf(1));
const branch = new Composite();
branch.add(new Leaf(2));
branch.add(new Leaf(3));
root.add(branch); // one real nested level
console.log(root.operation()); // 6
