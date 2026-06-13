// AFTER, classical form. Strategy as an interface + classes, and Template Method
// for the receipt skeleton. This is the form an agent most often produces when told
// only "use the Strategy pattern". (In TS, `implements` is optional — interfaces are
// structural — but we write it for intent.)

import { type Order, subtotal } from "./models";

// --- Strategy: each discount rule behind a common interface -----------------

export interface DiscountRule {
  apply(order: Order): number;
}

export class NoDiscount implements DiscountRule {
  apply(order: Order): number {
    return subtotal(order);
  }
}

export class PercentageOff implements DiscountRule {
  constructor(private readonly rate: number) {}
  apply(order: Order): number {
    return subtotal(order) * (1 - this.rate);
  }
}

export class CouponOff implements DiscountRule {
  constructor(private readonly amount: number) {}
  apply(order: Order): number {
    return Math.max(subtotal(order) - this.amount, 0);
  }
}

export class MemberDiscount implements DiscountRule {
  apply(order: Order): number {
    return order.isMember ? subtotal(order) * 0.85 : subtotal(order);
  }
}

export function applyDiscount(order: Order, rule: DiscountRule): number {
  return rule.apply(order);
}

// --- Template Method: fixed receipt skeleton, varying steps -----------------

export abstract class ReceiptRenderer {
  render(order: Order): string {
    // The fixed skeleton. Subclasses supply steps, never the order of steps.
    return [this.header(), this.lineItems(order), this.footer(order)].join("\n");
  }

  protected abstract header(): string;
  protected abstract lineItems(order: Order): string;

  protected footer(order: Order): string {
    // Hook: sensible default, override only if the format needs to.
    return `Total: ${subtotal(order).toFixed(2)}`;
  }
}

export class PlainTextReceipt extends ReceiptRenderer {
  protected header(): string {
    return "CHECKOUT-LITE RECEIPT";
  }
  protected lineItems(order: Order): string {
    return order.items
      .map((item) => `${item.name.padEnd(20)} ${item.price.toFixed(2).padStart(8)}`)
      .join("\n");
  }
}

export class HtmlReceipt extends ReceiptRenderer {
  protected header(): string {
    return "<h1>Checkout-lite receipt</h1>";
  }
  protected lineItems(order: Order): string {
    const rows = order.items
      .map((item) => `<tr><td>${item.name}</td><td>${item.price.toFixed(2)}</td></tr>`)
      .join("");
    return `<table>${rows}</table>`;
  }
  protected override footer(order: Order): string {
    return `<p>Total: ${subtotal(order).toFixed(2)}</p>`;
  }
}
