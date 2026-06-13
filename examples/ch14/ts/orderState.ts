// Chapter 14 · State: the order lifecycle as states that own their transitions.
//
// Each state is a class that knows which transitions are legal. Illegal moves
// (shipping an unpaid order) throw instead of silently corrupting a status string.

export class IllegalTransition extends Error {}

export interface OrderState {
  readonly name: string;
  pay(order: Order): void;
  ship(order: Order): void;
  cancel(order: Order): void;
}

// Base state: every transition is illegal by default; states allow some.
abstract class BaseState implements OrderState {
  abstract readonly name: string;
  pay(_order: Order): void {
    throw new IllegalTransition(`cannot pay from ${this.name}`);
  }
  ship(_order: Order): void {
    throw new IllegalTransition(`cannot ship from ${this.name}`);
  }
  cancel(_order: Order): void {
    throw new IllegalTransition(`cannot cancel from ${this.name}`);
  }
}

class Cart extends BaseState {
  readonly name = "cart";
  override pay(order: Order): void {
    order.state = new Paid();
  }
  override cancel(order: Order): void {
    order.state = new Cancelled();
  }
}

class Paid extends BaseState {
  readonly name = "paid";
  override ship(order: Order): void {
    order.state = new Shipped();
  }
  override cancel(order: Order): void {
    order.state = new Cancelled();
  }
}

class Shipped extends BaseState {
  readonly name = "shipped"; // terminal: nothing overridden, so all throw
}

class Cancelled extends BaseState {
  readonly name = "cancelled"; // terminal
}

export class Order {
  state: OrderState = new Cart();
  pay(): void {
    this.state.pay(this);
  }
  ship(): void {
    this.state.ship(this);
  }
  cancel(): void {
    this.state.cancel(this);
  }
  get status(): string {
    return this.state.name;
  }
}
