// BEFORE: the tangle. Several algorithms trapped in one body — every new discount
// edits applyDiscount, and the two receipt renderers duplicate the same skeleton.

import { type Order, subtotal } from "./models";

export function applyDiscount(order: Order, kind: string): number {
  switch (kind) {
    case "none":
      return subtotal(order);
    case "tenPercent":
      return subtotal(order) * 0.9;
    case "coupon5":
      return Math.max(subtotal(order) - 5, 0);
    case "member":
      return order.isMember ? subtotal(order) * 0.85 : subtotal(order);
    default:
      throw new Error(`unknown discount: ${kind}`);
  }
}

export function renderTextReceipt(order: Order): string {
  const lines = ["CHECKOUT-LITE RECEIPT"]; // header
  for (const item of order.items) {
    // line items
    lines.push(`${item.name.padEnd(20)} ${item.price.toFixed(2).padStart(8)}`);
  }
  lines.push(`Total: ${subtotal(order).toFixed(2)}`); // footer
  return lines.join("\n");
}

export function renderHtmlReceipt(order: Order): string {
  const rows = order.items
    .map((item) => `<tr><td>${item.name}</td><td>${item.price.toFixed(2)}</td></tr>`)
    .join("");
  return [
    "<h1>Checkout-lite receipt</h1>", // header
    `<table>${rows}</table>`, // line items
    `<p>Total: ${subtotal(order).toFixed(2)}</p>`, // footer — same shape, duplicated
  ].join("\n");
}
