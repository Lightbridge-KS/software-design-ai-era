"""Behavioral contract for the settings exercise.

These tests pin only the behavior that matters: defaults, environment
override, and types — through the public `get_settings()` API. They say
nothing about providers, chains, factories, or singletons. What the tests
don't pin is up for deletion.
"""

import pytest

import settings


@pytest.fixture(autouse=True)
def fresh_settings(monkeypatch: pytest.MonkeyPatch):
    """Each test starts with no cache and a clean environment."""
    for key in ("CHECKOUT_CURRENCY", "CHECKOUT_TAX_RATE", "CHECKOUT_RECEIPT_FORMAT"):
        monkeypatch.delenv(key, raising=False)
    if hasattr(settings, "SettingsFactory"):
        settings.SettingsFactory.reset()
    yield


def test_defaults() -> None:
    s = settings.get_settings()
    assert s.currency == "USD"
    assert s.tax_rate == 0.07
    assert s.receipt_format == "text"


def test_environment_overrides_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHECKOUT_CURRENCY", "THB")
    s = settings.get_settings()
    assert s.currency == "THB"
    assert s.tax_rate == 0.07  # untouched keys keep their defaults


def test_tax_rate_is_a_float(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHECKOUT_TAX_RATE", "0.10")
    assert settings.get_settings().tax_rate == 0.10


def test_settings_are_immutable() -> None:
    s = settings.get_settings()
    with pytest.raises(Exception):
        s.currency = "EUR"  # type: ignore[misc]
