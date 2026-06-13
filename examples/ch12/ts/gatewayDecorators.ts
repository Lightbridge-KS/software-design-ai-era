// Chapter 12 · Decorator: add behavior to a gateway without editing it.
//
// Each decorator implements IPaymentGateway and wraps ONE gateway, forwarding
// charge() while adding a cross-cutting concern. Decorators stack at runtime:
// new RetryingGateway(new LoggingGateway(new StripeGateway(), log)).

export interface Receipt {
  readonly provider: string;
  readonly amount: number;
  readonly confirmation: string;
}

export interface IPaymentGateway {
  charge(amount: number): Receipt;
}

export class TransientError extends Error {}

// The real gateway — the concrete component we wrap.
export class StripeGateway implements IPaymentGateway {
  charge(amount: number): Receipt {
    return { provider: "stripe", amount, confirmation: `ch_${Math.round(amount * 100)}` };
  }
}

// Base decorator: holds ONE wrapped gateway, forwards by default.
export class GatewayDecorator implements IPaymentGateway {
  constructor(protected readonly wrapped: IPaymentGateway) {}
  charge(amount: number): Receipt {
    return this.wrapped.charge(amount);
  }
}

export class LoggingGateway extends GatewayDecorator {
  constructor(
    wrapped: IPaymentGateway,
    private readonly log: string[],
  ) {
    super(wrapped);
  }
  override charge(amount: number): Receipt {
    this.log.push(`charging ${amount.toFixed(2)}`);
    const receipt = this.wrapped.charge(amount);
    this.log.push(`charged ${receipt.confirmation}`);
    return receipt;
  }
}

export class RetryingGateway extends GatewayDecorator {
  constructor(
    wrapped: IPaymentGateway,
    private readonly retries: number = 2,
  ) {
    super(wrapped);
  }
  override charge(amount: number): Receipt {
    let last: unknown;
    for (let attempt = 0; attempt <= this.retries; attempt++) {
      try {
        return this.wrapped.charge(amount);
      } catch (err) {
        if (!(err instanceof TransientError)) throw err; // only retry transients
        last = err;
      }
    }
    throw last; // retries exhausted
  }
}
