// Façade — canonical conceptual example. Run: npx tsx conceptFacade.ts
//
// A subsystem of several parts, each with its own API, behind one simple
// interface that coordinates them. In TS, a module-level function is a façade
// too — no class required.

export class SubsystemA {
  opA(): string {
    return "A";
  }
}

export class SubsystemB {
  opB(): string {
    return "B";
  }
}

export class SubsystemC {
  opC(): string {
    return "C";
  }
}

// --- Canonical: a Façade object that coordinates the subsystems -------------

export class Facade {
  private readonly a = new SubsystemA();
  private readonly b = new SubsystemB();
  private readonly c = new SubsystemC();

  operation(): string {
    return this.a.opA() + this.b.opB() + this.c.opC();
  }
}

// --- Idiomatic: a free function is a façade too — no class required ----------

export const operation = (): string =>
  new SubsystemA().opA() + new SubsystemB().opB() + new SubsystemC().opC();

// Demo
console.log(new Facade().operation()); // ABC
console.log(operation()); // ABC
