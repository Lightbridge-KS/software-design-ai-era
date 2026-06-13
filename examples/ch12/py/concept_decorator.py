"""Decorator — canonical conceptual example (runnable).

A Component interface; a ConcreteComponent; a Decorator that holds ONE component
and implements the same interface, adding behavior around the delegated call.
Decorators stack at runtime because each one IS a Component.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def operation(self) -> str: ...


class ConcreteComponent(Component):
    def operation(self) -> str:
        return "core"


class Decorator(Component):
    def __init__(self, wrapped: Component) -> None:
        self._wrapped = wrapped

    def operation(self) -> str:
        return self._wrapped.operation()  # base forwards; subclasses augment


class LoudDecorator(Decorator):
    def operation(self) -> str:
        return f"LOUD({self._wrapped.operation()})"  # augment one component


if __name__ == "__main__":
    stacked = LoudDecorator(LoudDecorator(ConcreteComponent()))
    print(stacked.operation())  # LOUD(LOUD(core)) — stacked at runtime
