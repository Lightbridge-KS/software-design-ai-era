"""Iterator — canonical conceptual example (runnable).

The classical form implements __iter__/__next__. The Pythonic form is a
generator — the same protocol, written with yield.
"""

from __future__ import annotations

from collections.abc import Iterator


class CountUp:
    """Classical iterator: explicit __iter__/__next__."""

    def __init__(self, limit: int) -> None:
        self._limit = limit
        self._n = 0

    def __iter__(self) -> CountUp:
        return self

    def __next__(self) -> int:
        if self._n >= self._limit:
            raise StopIteration
        self._n += 1
        return self._n


def count_up(limit: int) -> Iterator[int]:
    """Pythonic iterator: a generator does the same with yield."""
    for n in range(1, limit + 1):
        yield n


if __name__ == "__main__":
    print(list(CountUp(3)))   # [1, 2, 3]
    print(list(count_up(3)))  # [1, 2, 3]
