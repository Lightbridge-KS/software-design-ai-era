// Chapter 10 · Singleton, demoted.
//
// When you genuinely want one shared instance, the idiomatic form is a
// module-level object: an ES module is itself a singleton — evaluated once and
// cached — so the instance is created once and shared by every importer, with
// no class machinery and no global-access ceremony.

export class GatewayPool {
  // Something you might want exactly one of — a shared resource pool.
  constructor(readonly name: string = "default-pool") {}
}

// The idiomatic singleton: one instance, importable everywhere, swappable in tests.
export const pool = new GatewayPool();

export class SingletonPool {
  // The Singleton *pattern* — more machinery for the same one-instance result.
  // Rarely worth it, and it makes substitution in tests awkward.
  private static instance: SingletonPool | undefined;

  private constructor() {}

  static getInstance(): SingletonPool {
    if (SingletonPool.instance === undefined) {
      SingletonPool.instance = new SingletonPool();
    }
    return SingletonPool.instance;
  }
}
