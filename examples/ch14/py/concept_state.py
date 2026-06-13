"""State — canonical conceptual example (runnable).

A Context delegates to its current State object; each State implements the
operation and decides the next state. Behavior changes with state, with no
conditionals in the Context.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def handle(self, ctx: Context) -> str: ...


class Active(State):
    def handle(self, ctx: Context) -> str:
        ctx.state = Done()
        return "active->done"


class Done(State):
    def handle(self, ctx: Context) -> str:
        return "done"


class Context:
    def __init__(self) -> None:
        self.state: State = Active()

    def request(self) -> str:
        return self.state.handle(self)


if __name__ == "__main__":
    ctx = Context()
    print(ctx.request())  # active->done
    print(ctx.request())  # done
