// Chapter 8 · BEFORE: closed for extension, open for modification — backwards.
//
// Every new payment provider means editing processPayment — the one function
// you least want to touch, and the one whose existing branches you most risk
// breaking.

export interface Receipt {
  readonly provider: string;
  readonly amount: number;
  readonly confirmation: string;
}

export function processPayment(method: string, amount: number): Receipt {
  switch (method) {
    case "card":
      return { provider: "card", amount, confirmation: `card-${Math.round(amount * 100)}` };
    case "paypal":
      return { provider: "paypal", amount, confirmation: `pp-${Math.round(amount * 100)}` };
    default:
      throw new Error(`unknown payment method: ${method}`);
  }
}
