"""Adapter — canonical conceptual example (runnable).

A Target interface the client expects, an Adaptee with an incompatible API
(typically code you don't own), and an Adapter that implements Target by
translating to the Adaptee.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Target(ABC):
    @abstractmethod
    def request(self) -> str: ...


class Adaptee:
    """Existing/foreign class with an incompatible interface."""

    def specific_request(self) -> str:
        return "data-from-adaptee"


class Adapter(Target):
    def __init__(self, adaptee: Adaptee) -> None:
        self._adaptee = adaptee

    def request(self) -> str:
        raw = self._adaptee.specific_request()
        return f"translated({raw})"   # the real work: translate to Target's shape


def client(target: Target) -> str:
    return target.request()           # the client only knows Target


if __name__ == "__main__":
    print(client(Adapter(Adaptee())))  # translated(data-from-adaptee)
