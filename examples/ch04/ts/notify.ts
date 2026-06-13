// Notification — answers to one actor: marketing (the receipt message). One reason
// to change: what the customer is told, and how. The email I/O is isolated here,
// away from the money math.

import { appendFileSync } from "node:fs";
import { type Order } from "./models";

// Pure: the message text. Marketing owns this; no I/O to test around.
export const receiptBody = (order: Order, total: number): string =>
  `Thanks ${order.customer.name}! You paid ${total.toFixed(2)}.`;

// The I/O edge. The "send" is faked as a local file append so the example runs with
// no SMTP server; failures never block a sale.
export const sendReceipt = (
  order: Order,
  total: number,
  outboxFile = "outbox.txt",
): void => {
  try {
    appendFileSync(outboxFile, `To: ${order.customer.email}\n${receiptBody(order, total)}\n`);
  } catch {
    // a failed email must never block a sale
  }
};
