// Chapter 14 tests — Observer and State, made executable. Mirrors the Python suite.
//
// Observer: every subscriber receives the published event, and no subscribers
// is fine. State: the lifecycle walks legal transitions and rejects illegal ones.

import { describe, expect, it } from "vitest";
import { OrderEvents, placeOrder, type OrderPlaced } from "./events";
import { IllegalTransition, Order } from "./orderState";

// --- Observer ---------------------------------------------------------------

describe("Observer: subscribers react to a published event", () => {
  it("notifies every subscriber in order", () => {
    const events = new OrderEvents();
    const seen: string[] = [];
    events.subscribe((e) => seen.push(`receipt:${e.orderId}`));
    events.subscribe((e) => seen.push(`inventory:${e.total}`));
    placeOrder("A1", 30, events);
    expect(seen).toEqual(["receipt:A1", "inventory:30"]);
  });

  it("works with no subscribers", () => {
    const events = new OrderEvents();
    const event: OrderPlaced = placeOrder("A2", 10, events);
    expect(event).toEqual({ orderId: "A2", total: 10 });
  });
});

// --- State ------------------------------------------------------------------

describe("State: the lifecycle enforces legal transitions", () => {
  it("walks the happy path cart -> paid -> shipped", () => {
    const order = new Order();
    expect(order.status).toBe("cart");
    order.pay();
    expect(order.status).toBe("paid");
    order.ship();
    expect(order.status).toBe("shipped");
  });

  it("rejects an illegal transition", () => {
    const order = new Order();
    expect(() => order.ship()).toThrow(IllegalTransition); // cannot ship from cart
  });

  it("can cancel from cart and from paid", () => {
    const fromCart = new Order();
    fromCart.cancel();
    expect(fromCart.status).toBe("cancelled");

    const fromPaid = new Order();
    fromPaid.pay();
    fromPaid.cancel();
    expect(fromPaid.status).toBe("cancelled");
  });
});
