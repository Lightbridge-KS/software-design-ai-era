// Visitor — canonical conceptual example. Run: npx tsx conceptVisitor.ts
//
// Double dispatch: element.accept(visitor) calls back visitor.visitX(this). The
// modern replacement is a discriminated union + exhaustive switch.

export interface Visitor<T> {
  visitA(element: ElementA): T;
  visitB(element: ElementB): T;
}

export interface Element {
  accept<T>(visitor: Visitor<T>): T;
}

export class ElementA implements Element {
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitA(this);
  }
}

export class ElementB implements Element {
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitB(this);
  }
}

export class NameVisitor implements Visitor<string> {
  visitA(_element: ElementA): string {
    return "A";
  }
  visitB(_element: ElementB): string {
    return "B";
  }
}

// Demo
const elements: Element[] = [new ElementA(), new ElementB()];
console.log(elements.map((e) => e.accept(new NameVisitor()))); // ['A', 'B']
