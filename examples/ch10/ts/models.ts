// Shared checkout-lite payment model. A Receipt is plain readonly data; the
// IPaymentGateway interface is the seam Chapter 8 injected. Real money wants
// integer cents; number keeps these teaching examples short.

export interface Receipt {
  readonly provider: string;
  readonly amount: number;
}

export interface IPaymentGateway {
  charge(amount: number): Receipt;
}

export class CardGateway implements IPaymentGateway {
  charge(amount: number): Receipt {
    return { provider: "card", amount };
  }
}

export class PayPalGateway implements IPaymentGateway {
  charge(amount: number): Receipt {
    return { provider: "paypal", amount };
  }
}
