// Chapter 11 · Adapter: make third-party code fit an interface we own.
//
// The SDK we don't own speaks cents and plain objects; our codebase speaks
// dollars and Receipts. The adapter implements our interface and translates —
// so Stripe's shape never leaks past this one class.

export interface Receipt {
  readonly provider: string;
  readonly amount: number;
  readonly confirmation: string;
}

// Our target interface. We own both sides, so we declare it and `implements` it
// for intent — though TS would accept a structural match without the keyword.
export interface IPaymentGateway {
  charge(amount: number): Receipt;
}

// A third-party SDK we do NOT own — different method, cents, returns a record.
export class StripeClient {
  createCharge(amountCents: number, currency = "usd"): Record<string, unknown> {
    return { id: `ch_${amountCents}`, paid: true, currency };
  }
}

// The Adapter: fits our interface, delegates and translates to the adaptee.
export class StripeGateway implements IPaymentGateway {
  constructor(private readonly client: StripeClient) {}
  charge(amount: number): Receipt {
    const resp = this.client.createCharge(Math.round(amount * 100)); // dollars → cents
    return { provider: "stripe", amount, confirmation: String(resp.id) }; // record → Receipt
  }
}

// Depend on a shape, not a base class — for code we can't make inherit ours.
// In TS this is just an interface: structural typing makes it a Protocol-equivalent.
export interface SupportsCharge {
  charge(amount: number): Receipt;
}

// Inherits nothing of ours, declares no `implements` — yet already matches
// SupportsCharge by shape, so it needs no adapter at all.
export class InHouseGateway {
  charge(amount: number): Receipt {
    return { provider: "inhouse", amount, confirmation: `ih-${Math.round(amount * 100)}` };
  }
}
