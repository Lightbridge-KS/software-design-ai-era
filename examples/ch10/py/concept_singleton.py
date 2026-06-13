"""Singleton — canonical conceptual example (runnable).

The classical Singleton ensures one instance with global access. The Pythonic
form needs none of it: a module is already a singleton, so a module-level
instance gives the same guarantee and stays injectable for tests.
"""

from __future__ import annotations


# --- Canonical: the Singleton pattern ---------------------------------------

class Singleton:
    _instance: Singleton | None = None

    def __new__(cls) -> Singleton:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# --- Pythonic: a module-level instance (this object, imported, IS the singleton)

class Config:
    def __init__(self) -> None:
        self.theme = "light"


config = Config()   # created once at import; `from concept_singleton import config`


if __name__ == "__main__":
    print(Singleton() is Singleton())   # True — but it took a __new__ to get here
    print(config is config)             # True — and this needed no machinery
