// Chapter 8 · AFTER: open for extension via an injected interface.
//
// processPayment depends on the IPaymentGateway abstraction, not on concrete
// providers. Adding a provider is a new class; the core is never edited.
//
// The cross-language lesson lives here: in Python you must CHOOSE between a
// nominal interface (an ABC you inherit) and a structural one (a Protocol that
// matches by shape). In TypeScript that choice is gone — interfaces are
// structural by default. A class satisfies IPaymentGateway whether or not it
// writes `implements`, and a foreign object with the right shape just fits.

export interface Receipt {
  readonly provider: string;
  readonly amount: number;
  readonly confirmation: string;
}

// Our target interface. We own both sides, so we write `implements` on our
// gateways below for intent and a clearer compiler error — but TS would accept
// a structural match without the keyword (see InHouseGateway).
export interface IPaymentGateway {
  // Charge `amount`. Postcondition: returns a Receipt for that amount.
  charge(amount: number): Receipt;
}

export class CardGateway implements IPaymentGateway {
  charge(amount: number): Receipt {
    return { provider: "card", amount, confirmation: `card-${Math.round(amount * 100)}` };
  }
}

export class PayPalGateway implements IPaymentGateway {
  charge(amount: number): Receipt {
    return { provider: "paypal", amount, confirmation: `pp-${Math.round(amount * 100)}` };
  }
}

// Open for extension: a new gateway is a new class, not an edit here.
export function processPayment(gateway: IPaymentGateway, amount: number): Receipt {
  return gateway.charge(amount);
}

// A Liskov violation: substitutable in name only — breaks the contract. It
// declares `implements`, so it type-checks, yet returns null at runtime. We
// cast to escape the compiler the way the Python version uses `# type: ignore`.
export class BadGateway implements IPaymentGateway {
  charge(_amount: number): Receipt {
    return null as unknown as Receipt; // violates the postcondition
  }
}

// In Python this point needs a separate `Protocol`; in TS the interface above
// is ALREADY structural, so we reuse the shape. A class that never declares
// `implements` and inherits nothing of ours still satisfies it — by shape alone.
export class InHouseGateway {
  charge(amount: number): Receipt {
    return { provider: "inhouse", amount, confirmation: `ih-${Math.round(amount * 100)}` };
  }
}

// A foreign object — a plain object literal, no class, no inheritance — also
// fits IPaymentGateway the moment it has a matching `charge`. Structural typing
// is what lets `process` accept it untouched.
export const thirdPartyWallet: IPaymentGateway = {
  charge(amount: number): Receipt {
    return { provider: "wallet", amount, confirmation: `w-${Math.round(amount * 100)}` };
  },
};
