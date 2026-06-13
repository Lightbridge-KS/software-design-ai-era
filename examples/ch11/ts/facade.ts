// Chapter 11 · Façade: one friendly door over the checkout subsystems.
//
// Placing an order means coordinating four subsystems. The façade hides that
// dance behind a single call, so callers depend on one simple thing.

export interface LineItem {
  readonly name: string;
  readonly price: number;
}

export interface Order {
  readonly items: readonly LineItem[];
}

export interface Receipt {
  readonly total: number;
  readonly confirmation: string;
}

const subtotal = (order: Order): number =>
  order.items.reduce((sum, item) => sum + item.price, 0);

// --- the subsystems (each cohesive; see Chapters 4-10) ----------------------

export const orderTotal = (order: Order): number =>
  Math.round(subtotal(order) * 1.07 * 100) / 100; // pricing (+7% tax, simplified)

export const charge = (total: number): string => `ch_${Math.round(total * 100)}`; // gateway

export const sendReceipt = (_order: Order, _total: number): void => {
  // Notification subsystem (I/O elided).
};

export const saveOrder = (_order: Order, _total: number): void => {
  // Persistence subsystem (I/O elided).
};

// --- the Façade: one call hides the four-step orchestration -----------------

export const placeOrder = (order: Order): Receipt => {
  const total = orderTotal(order);
  const confirmation = charge(total);
  sendReceipt(order, total);
  saveOrder(order, total);
  return { total, confirmation };
};
