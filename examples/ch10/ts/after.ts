// AFTER: one factory function, backed by a registry. A class is already a
// callable that constructs an instance — so a `Record` of constructor thunks
// *is* a factory. Construction knowledge lives in one place; adding a provider
// is one registry entry, and every call site just asks makeGateway.

import { type IPaymentGateway, type Receipt, CardGateway, PayPalGateway } from "./models";

// The registry: map each key to a thunk that builds the concrete gateway.
// (`() => new CardGateway()` is the callable; the bare class reference works too.)
export const GATEWAYS: Record<string, () => IPaymentGateway> = {
  card: () => new CardGateway(),
  paypal: () => new PayPalGateway(),
};

export function makeGateway(method: string): IPaymentGateway {
  const build = GATEWAYS[method];
  if (build === undefined) {
    throw new Error(`unknown payment method: ${method}`); // unknown -> fail fast
  }
  return build();
}

export function checkout(method: string, amount: number): Receipt {
  return makeGateway(method).charge(amount);
}

export function refund(method: string, amount: number): Receipt {
  return makeGateway(method).charge(-amount);
}
