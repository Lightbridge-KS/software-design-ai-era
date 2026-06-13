// BEFORE: construction scattered across call sites. Chapter 8 made *using* a
// gateway open-closed by injecting it — but something still has to *build* the
// right one, and that switch is now copy-pasted wherever a gateway is needed.

import { type IPaymentGateway, type Receipt, CardGateway, PayPalGateway } from "./models";

export function checkout(method: string, amount: number): Receipt {
  let gateway: IPaymentGateway;
  if (method === "card") {
    gateway = new CardGateway();
  } else if (method === "paypal") {
    gateway = new PayPalGateway();
  } else {
    throw new Error(`unknown payment method: ${method}`);
  }
  return gateway.charge(amount);
}

export function refund(method: string, amount: number): Receipt {
  let gateway: IPaymentGateway;
  if (method === "card") {
    // the same switch, copied
    gateway = new CardGateway();
  } else if (method === "paypal") {
    gateway = new PayPalGateway();
  } else {
    throw new Error(`unknown payment method: ${method}`);
  }
  return gateway.charge(-amount);
}
