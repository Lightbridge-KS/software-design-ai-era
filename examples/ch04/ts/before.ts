// BEFORE: one function, four actors. checkout() changes for four unrelated reasons —
// finance (tax), ops (shipping), marketing (email copy), engineering (storage). That
// is four reasons to change in one body: the structural definition of "does too much".

import { appendFileSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import { type Order, subtotal } from "./models";

// The email "send" is faked as a local file append so the example runs with no SMTP
// server — the point is that an I/O concern is tangled into the money math, not the
// transport. Failures must never block a sale.
export function checkout(
  order: Order,
  paymentToken: string,
  sendEmail = true,
  ordersFile = "orders.json",
  outboxFile = "outbox.txt",
): number {
  let total = subtotal(order);
  if (order.customer.isMember) {
    total = total * 0.85;
  }

  if (order.country === "US") {
    total = total + total * 0.07;
  } else if (order.country === "DE") {
    total = total + total * 0.19;
  } else if (order.country === "JP") {
    total = total + total * 0.1;
  }

  if (order.country === "US") {
    total = total + 5.0;
  } else if (["DE", "FR", "NL"].includes(order.country)) {
    total = total + 9.9;
  } else {
    total = total + 24.9;
  }
  if (order.giftWrap) {
    total = total + 3.5;
  }

  total = Math.round(total * 100) / 100;
  console.log(`Charging ${paymentToken} for ${total.toFixed(2)}`);

  if (order.customer.isMember && sendEmail) {
    try {
      const body = `Thanks ${order.customer.name}! You paid ${total.toFixed(2)}.`;
      appendFileSync(outboxFile, `To: ${order.customer.email}\n${body}\n`);
    } catch {
      // a failed email must never block a sale
    }
  }

  const record = { customer: order.customer.name, total };
  const existing: unknown[] = existsSync(ordersFile)
    ? (JSON.parse(readFileSync(ordersFile, "utf8")) as unknown[])
    : [];
  existing.push(record);
  writeFileSync(ordersFile, JSON.stringify(existing, null, 2));
  return total;
}
