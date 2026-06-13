// Singleton — canonical conceptual example. Run: npx tsx conceptSingleton.ts
//
// The classical Singleton ensures one instance with global access. The
// idiomatic form needs none of it: an ES module is itself a singleton —
// evaluated once and cached — so a module-level instance gives the same
// guarantee and stays injectable for tests.

// --- Canonical: the Singleton pattern (rarely needed) -----------------------

export class Singleton {
  private static instance: Singleton | undefined;

  // A private constructor blocks `new Singleton()` from outside.
  private constructor() {}

  static getInstance(): Singleton {
    if (Singleton.instance === undefined) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }
}

// --- Idiomatic: a module-level instance (this object, imported, IS the singleton)

export class Config {
  theme = "light";
}

export const config = new Config(); // created once at module load; importable everywhere

// Demo
console.log(Singleton.getInstance() === Singleton.getInstance()); // true — but it took machinery
console.log(config === config); // true — and this needed none
