"""Strategy — canonical conceptual example (runnable).

Encapsulate interchangeable algorithms behind a common interface and inject the
chosen one. The canonical class form is what the name denotes; in Python a
strategy is usually just a function in a registry.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable


# --- Canonical: a Strategy interface, injected into a Context ----------------

class Strategy(ABC):
    @abstractmethod
    def execute(self, data: list[int]) -> list[int]: ...


class AscendingStrategy(Strategy):
    def execute(self, data: list[int]) -> list[int]:
        return sorted(data)


class DescendingStrategy(Strategy):
    def execute(self, data: list[int]) -> list[int]:
        return sorted(data, reverse=True)


class Context:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def do_work(self, data: list[int]) -> list[int]:
        return self._strategy.execute(data)   # delegates to the injected strategy


# --- Pythonic: a strategy is a function; a registry selects one --------------

SortStrategy = Callable[[list[int]], list[int]]

STRATEGIES: dict[str, SortStrategy] = {
    "asc": sorted,
    "desc": lambda d: sorted(d, reverse=True),
}


if __name__ == "__main__":
    print(Context(DescendingStrategy()).do_work([3, 1, 2]))  # [3, 2, 1]
    print(STRATEGIES["asc"]([3, 1, 2]))                       # [1, 2, 3]
