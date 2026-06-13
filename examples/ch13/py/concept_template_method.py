"""Template Method — canonical conceptual example (runnable).

Fix an algorithm's skeleton in a base method; let subclasses fill in the steps
(and optionally override hooks). The skeleton's order is the invariant subclasses
cannot change.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractFlow(ABC):
    def run(self) -> list[str]:
        """The template method: the fixed skeleton. Subclasses never override this."""
        return [self.step_one(), self.step_two(), self.hook()]

    @abstractmethod
    def step_one(self) -> str: ...

    @abstractmethod
    def step_two(self) -> str: ...

    def hook(self) -> str:
        """A hook: a default step, optional to override."""
        return "default"


class ConcreteFlow(AbstractFlow):
    def step_one(self) -> str:
        return "one"

    def step_two(self) -> str:
        return "two"


class CustomFlow(AbstractFlow):
    def step_one(self) -> str:
        return "1"

    def step_two(self) -> str:
        return "2"

    def hook(self) -> str:        # overrides the optional hook
        return "custom"


if __name__ == "__main__":
    print(ConcreteFlow().run())   # ['one', 'two', 'default']
    print(CustomFlow().run())     # ['1', '2', 'custom']
