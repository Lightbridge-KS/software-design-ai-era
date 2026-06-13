"""Visitor — canonical conceptual example (runnable).

Double dispatch: element.accept(visitor) calls back visitor.visit_x(self), so
the right operation runs for the right type. The modern replacement is a single
function using structural match (see total_via_match in visitor.py).
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Visitor(ABC):
    @abstractmethod
    def visit_a(self, element: ElementA) -> str: ...

    @abstractmethod
    def visit_b(self, element: ElementB) -> str: ...


class Element(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> str: ...


class ElementA(Element):
    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_a(self)


class ElementB(Element):
    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_b(self)


class NameVisitor(Visitor):
    def visit_a(self, element: ElementA) -> str:
        return "A"

    def visit_b(self, element: ElementB) -> str:
        return "B"


if __name__ == "__main__":
    elements: list[Element] = [ElementA(), ElementB()]
    print([e.accept(NameVisitor()) for e in elements])  # ['A', 'B']
