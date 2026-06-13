// Checkout — answers to one actor: the order workflow itself. One reason to change:
// the *sequence* of steps. It owns orchestration, not the steps' internals. Each
// concern lives in its own cohesive file; this function reads like a table of contents.

import { type Order } from "./models";
import { orderTotal } from "./pricing";
import { sendReceipt } from "./notify";
import { saveOrder } from "./persistence";

export const checkout = (
  order: Order,
  paymentToken: string,
  sendEmail = true,
  ordersFile = "orders.json",
  outboxFile = "outbox.txt",
): number => {
  const total = orderTotal(order);
  console.log(`Charging ${paymentToken} for ${total.toFixed(2)}`);
  if (order.customer.isMember && sendEmail) {
    sendReceipt(order, total, outboxFile);
  }
  saveOrder(order, total, ordersFile);
  return total;
};
