// Behavioral contract for the settings exercise.
//
// These tests pin only the behavior that matters: defaults, environment override,
// and types — through the public `getSettings()` API. They say nothing about
// providers, chains, factories, or singletons. What the tests don't pin is up for
// deletion.

import { afterEach, beforeEach, describe, expect, it } from "vitest";
import * as settings from "./settings";

const ENV_KEYS = ["CHECKOUT_CURRENCY", "CHECKOUT_TAXRATE", "CHECKOUT_RECEIPTFORMAT"];

// Each test starts with no cache and a clean environment.
beforeEach(() => {
  for (const key of ENV_KEYS) {
    delete process.env[key];
  }
  settings.SettingsFactory?.reset();
});

afterEach(() => {
  for (const key of ENV_KEYS) {
    delete process.env[key];
  }
  settings.SettingsFactory?.reset();
});

describe("settings: the behavioral contract, not the structure", () => {
  it("defaults", () => {
    const s = settings.getSettings();
    expect(s.currency).toBe("USD");
    expect(s.taxRate).toBe(0.07);
    expect(s.receiptFormat).toBe("text");
  });

  it("environment overrides defaults", () => {
    process.env.CHECKOUT_CURRENCY = "THB";
    const s = settings.getSettings();
    expect(s.currency).toBe("THB");
    expect(s.taxRate).toBe(0.07); // untouched keys keep their defaults
  });

  it("tax rate is a number", () => {
    process.env.CHECKOUT_TAXRATE = "0.10";
    expect(settings.getSettings().taxRate).toBe(0.1);
  });

  it("settings are immutable", () => {
    const s = settings.getSettings();
    expect(() => {
      // @ts-expect-error -- readonly fields must not be assignable
      s.currency = "EUR";
    }).toThrow();
  });
});
