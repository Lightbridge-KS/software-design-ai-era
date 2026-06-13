// Adapter — canonical conceptual example. Run: npx tsx conceptAdapter.ts
//
// A Target interface the client expects, an Adaptee with an incompatible API
// (typically code you don't own), and an Adapter that implements Target by
// translating to the Adaptee.

// --- Canonical: an Adapter wrapping an incompatible Adaptee -----------------

export interface Target {
  request(): string;
}

export class Adaptee {
  // Existing/foreign class with an incompatible interface.
  specificRequest(): string {
    return "data-from-adaptee";
  }
}

export class Adapter implements Target {
  constructor(private readonly adaptee: Adaptee) {}
  request(): string {
    const raw = this.adaptee.specificRequest();
    return `translated(${raw})`; // the real work: translate to Target's shape
  }
}

export const client = (target: Target): string => target.request();

// --- Structural: a class already shaped like Target needs no adapter --------
// TS types are structural, so any object with a matching `request()` IS a Target.

export class AlreadyShaped {
  request(): string {
    return "native";
  }
}

// Demo
console.log(client(new Adapter(new Adaptee()))); // translated(data-from-adaptee)
console.log(client(new AlreadyShaped())); // native — satisfies Target by shape, no wrapper
