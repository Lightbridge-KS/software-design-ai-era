"""Façade — canonical conceptual example (runnable).

A subsystem of several parts, each with its own API, behind one simple
interface that coordinates them. In Python, a module-level function is a
façade too — no class required.
"""

from __future__ import annotations


class SubsystemA:
    def op_a(self) -> str:
        return "A"


class SubsystemB:
    def op_b(self) -> str:
        return "B"


class SubsystemC:
    def op_c(self) -> str:
        return "C"


class Facade:
    def __init__(self) -> None:
        self._a, self._b, self._c = SubsystemA(), SubsystemB(), SubsystemC()

    def operation(self) -> str:
        return self._a.op_a() + self._b.op_b() + self._c.op_c()


def operation() -> str:
    """The Pythonic façade: a function that coordinates the subsystems."""
    return SubsystemA().op_a() + SubsystemB().op_b() + SubsystemC().op_c()


if __name__ == "__main__":
    print(Facade().operation())  # ABC
    print(operation())           # ABC
