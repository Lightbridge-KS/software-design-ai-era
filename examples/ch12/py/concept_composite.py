"""Composite — canonical conceptual example (runnable).

A Component interface; a Leaf implements it directly; a Composite holds children
(each itself a Component) and delegates the operation to them, aggregating the
results. The client treats leaf and composite identically.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def operation(self) -> int: ...


class Leaf(Component):
    def __init__(self, value: int) -> None:
        self._value = value

    def operation(self) -> int:
        return self._value


class Composite(Component):
    def __init__(self) -> None:
        self._children: list[Component] = []

    def add(self, child: Component) -> None:
        self._children.append(child)

    def operation(self) -> int:
        return sum(child.operation() for child in self._children)  # aggregate


if __name__ == "__main__":
    root = Composite()
    root.add(Leaf(1))
    branch = Composite()
    branch.add(Leaf(2))
    branch.add(Leaf(3))
    root.add(branch)            # one real nested level
    print(root.operation())     # 6
