"""Chapter 10 · Singleton, demoted.

When you genuinely want one shared instance, the Pythonic form is a
module-level object: a module is itself a singleton — imported once and
cached — so the instance is created once and shared everywhere it is
imported, with no class machinery and no global-access ceremony.
"""

from dataclasses import dataclass


@dataclass
class GatewayPool:
    """Something you might want exactly one of — a shared resource pool."""

    name: str = "default-pool"


# The Pythonic singleton: one instance, importable everywhere, swappable in tests.
pool = GatewayPool()


class SingletonPool:
    """The Singleton *pattern* — more machinery for the same one-instance result.

    Rarely worth it in Python, and it makes substitution in tests awkward.
    """

    _instance: "SingletonPool | None" = None

    def __new__(cls) -> "SingletonPool":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
