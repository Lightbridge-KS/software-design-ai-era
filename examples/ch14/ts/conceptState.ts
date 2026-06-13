// State — canonical conceptual example. Run: npx tsx conceptState.ts
//
// A Context delegates to its current State; each State implements the operation
// and decides the next state. Behavior changes with state, no conditionals.

export interface State {
  handle(ctx: Context): string;
}

export class Active implements State {
  handle(ctx: Context): string {
    ctx.state = new Done();
    return "active->done";
  }
}

export class Done implements State {
  handle(_ctx: Context): string {
    return "done";
  }
}

export class Context {
  state: State = new Active();
  request(): string {
    return this.state.handle(this);
  }
}

// Demo
const ctx = new Context();
console.log(ctx.request()); // active->done
console.log(ctx.request()); // done
