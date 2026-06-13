// Template Method — canonical conceptual example. Run: npx tsx conceptTemplateMethod.ts
//
// Fix an algorithm's skeleton in a base method; let subclasses fill in the steps
// (and optionally override hooks). The skeleton's order is the invariant subclasses
// cannot change.

export abstract class AbstractFlow {
  run(): string[] {
    // The template method: the fixed skeleton. Subclasses never override this.
    return [this.stepOne(), this.stepTwo(), this.hook()];
  }

  protected abstract stepOne(): string;
  protected abstract stepTwo(): string;

  protected hook(): string {
    // A hook: a default step, optional to override.
    return "default";
  }
}

export class ConcreteFlow extends AbstractFlow {
  protected stepOne(): string {
    return "one";
  }
  protected stepTwo(): string {
    return "two";
  }
}

export class CustomFlow extends AbstractFlow {
  protected stepOne(): string {
    return "1";
  }
  protected stepTwo(): string {
    return "2";
  }
  protected override hook(): string {
    return "custom";
  }
}

// Demo
console.log(new ConcreteFlow().run()); // ["one", "two", "default"]
console.log(new CustomFlow().run()); // ["1", "2", "custom"]
