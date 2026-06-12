"""Chapter 9 exercise starter: checkout-lite's configuration "system".

Three values with defaults, served by a provider interface, a provider
chain, a factory, and a cached singleton. Your agent's job is to make
this module dramatically smaller while `test_settings.py` stays green.
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass


class ISettingsProvider(ABC):
    """Speculates: settings will someday come from files, vaults, services..."""

    @abstractmethod
    def get(self, key: str) -> str | None: ...


class EnvSettingsProvider(ISettingsProvider):
    def __init__(self, prefix: str = "CHECKOUT_") -> None:
        self._prefix = prefix

    def get(self, key: str) -> str | None:
        return os.environ.get(self._prefix + key.upper())


class DefaultSettingsProvider(ISettingsProvider):
    _DEFAULTS: dict[str, str] = {
        "currency": "USD",
        "tax_rate": "0.07",
        "receipt_format": "text",
    }

    def get(self, key: str) -> str | None:
        return self._DEFAULTS.get(key)


class ChainedSettingsProvider(ISettingsProvider):
    """First provider with an answer wins."""

    def __init__(self, providers: list[ISettingsProvider]) -> None:
        self._providers = providers

    def get(self, key: str) -> str | None:
        for provider in self._providers:
            value = provider.get(key)
            if value is not None:
                return value
        return None


@dataclass(frozen=True)
class Settings:
    currency: str
    tax_rate: float
    receipt_format: str


class SettingsFactory:
    """A factory, a chain, and a singleton — for three values with defaults."""

    _instance: Settings | None = None

    @classmethod
    def create(cls) -> Settings:
        if cls._instance is None:
            provider = ChainedSettingsProvider(
                [EnvSettingsProvider(), DefaultSettingsProvider()]
            )
            currency = provider.get("currency")
            tax_rate = provider.get("tax_rate")
            receipt_format = provider.get("receipt_format")
            assert currency is not None
            assert tax_rate is not None
            assert receipt_format is not None
            cls._instance = Settings(
                currency=currency,
                tax_rate=float(tax_rate),
                receipt_format=receipt_format,
            )
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        cls._instance = None


def get_settings() -> Settings:
    """The module's public API — the only thing callers actually use."""
    return SettingsFactory.create()
