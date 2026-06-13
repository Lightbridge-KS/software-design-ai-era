// Decorator — canonical conceptual example. Run: npx tsx conceptDecorator.ts
//
// A Component interface; a ConcreteComponent; a Decorator that holds ONE
// component and implements the same interface, adding behavior around the
// delegated call. Decorators stack at runtime because each one IS a Component.

export interface Component {
  operation(): string;
}

export class ConcreteComponent implements Component {
  operation(): string {
    return "core";
  }
}

export class Decorator implements Component {
  constructor(protected readonly wrapped: Component) {}
  operation(): string {
    return this.wrapped.operation(); // base forwards; subclasses augment
  }
}

export class LoudDecorator extends Decorator {
  override operation(): string {
    return `LOUD(${this.wrapped.operation()})`; // augment one component
  }
}

// Demo
const stacked = new LoudDecorator(new LoudDecorator(new ConcreteComponent()));
console.log(stacked.operation()); // LOUD(LOUD(core)) — stacked at runtime
