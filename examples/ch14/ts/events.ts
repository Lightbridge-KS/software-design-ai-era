// Chapter 14 · Observer: announce order events; subscribers react.
//
// The order flow publishes an event; interested parties subscribe without the
// flow knowing who they are. Adding a reaction is one subscribe() call — the
// core placeOrder code never changes.

export interface OrderPlaced {
  readonly orderId: string;
  readonly total: number;
}

export type Subscriber = (event: OrderPlaced) => void;

export class OrderEvents {
  private readonly subscribers: Subscriber[] = [];
  subscribe(subscriber: Subscriber): void {
    this.subscribers.push(subscriber);
  }
  publish(event: OrderPlaced): void {
    for (const subscriber of this.subscribers) subscriber(event);
  }
}

export const placeOrder = (
  orderId: string,
  total: number,
  events: OrderEvents,
): OrderPlaced => {
  const event: OrderPlaced = { orderId, total };
  events.publish(event); // do the work, then announce — who listens is not our concern
  return event;
};
