"""Observer — canonical conceptual example (runnable).

A Subject maintains a list of observers and notifies each on change. Observers
subscribe without the Subject knowing their concrete types.
"""

from __future__ import annotations

from collections.abc import Callable

Observer = Callable[[str], None]


class Subject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify(self, event: str) -> None:
        for observer in self._observers:
            observer(event)


if __name__ == "__main__":
    subject = Subject()
    subject.subscribe(lambda e: print(f"A saw {e}"))
    subject.subscribe(lambda e: print(f"B saw {e}"))
    subject.notify("ping")  # A saw ping / B saw ping
