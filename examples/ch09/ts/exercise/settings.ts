// Chapter 9 exercise starter: checkout-lite's configuration "system".
//
// Three values with defaults, served by a provider interface, a provider chain,
// a factory, and a cached singleton. Your agent's job is to make this module
// dramatically smaller while `settings.test.ts` stays green.

// Speculates: settings will someday come from files, vaults, services...
export interface ISettingsProvider {
  get(key: string): string | undefined;
}

export class EnvSettingsProvider implements ISettingsProvider {
  constructor(private readonly prefix = "CHECKOUT_") {}

  get(key: string): string | undefined {
    return process.env[this.prefix + key.toUpperCase()];
  }
}

export class DefaultSettingsProvider implements ISettingsProvider {
  private static readonly DEFAULTS: Record<string, string> = {
    currency: "USD",
    taxRate: "0.07",
    receiptFormat: "text",
  };

  get(key: string): string | undefined {
    return DefaultSettingsProvider.DEFAULTS[key];
  }
}

// First provider with an answer wins.
export class ChainedSettingsProvider implements ISettingsProvider {
  constructor(private readonly providers: readonly ISettingsProvider[]) {}

  get(key: string): string | undefined {
    for (const provider of this.providers) {
      const value = provider.get(key);
      if (value !== undefined) {
        return value;
      }
    }
    return undefined;
  }
}

export interface Settings {
  readonly currency: string;
  readonly taxRate: number;
  readonly receiptFormat: string;
}

// A factory, a chain, and a singleton — for three values with defaults.
export class SettingsFactory {
  private static instance: Settings | undefined = undefined;

  static create(): Settings {
    if (SettingsFactory.instance === undefined) {
      const provider = new ChainedSettingsProvider([
        new EnvSettingsProvider(),
        new DefaultSettingsProvider(),
      ]);
      const currency = provider.get("currency");
      const taxRate = provider.get("taxRate");
      const receiptFormat = provider.get("receiptFormat");
      if (currency === undefined || taxRate === undefined || receiptFormat === undefined) {
        throw new Error("missing required setting");
      }
      SettingsFactory.instance = Object.freeze({
        currency,
        taxRate: Number(taxRate),
        receiptFormat,
      });
    }
    return SettingsFactory.instance;
  }

  static reset(): void {
    SettingsFactory.instance = undefined;
  }
}

// The module's public API — the only thing callers actually use.
export function getSettings(): Settings {
  return SettingsFactory.create();
}
