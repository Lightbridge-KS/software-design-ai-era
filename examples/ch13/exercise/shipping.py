"""Chapter 10 exercise starter: the shipping-cost tangle.

Refactor with your agent using the "Strategy, right-sized" prompt from the
chapter (adapt the names), then grade the output with the review checklist.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Shipment:
    weight_kg: float
    destination_country: str
    declared_value: float


def shipping_cost(shipment: Shipment, carrier: str) -> float:
    """Return the shipping cost for the given carrier option."""
    if carrier == "standard":
        return 4.90 + 0.50 * shipment.weight_kg
    elif carrier == "express":
        base = 9.90 + 1.20 * shipment.weight_kg
        if shipment.declared_value > 100.0:
            base += 2.50  # mandatory insurance
        return base
    elif carrier == "pickup":
        return 0.0
    elif carrier == "international":
        if shipment.destination_country in ("DE", "FR", "NL"):
            return 14.90 + 1.00 * shipment.weight_kg
        return 24.90 + 2.20 * shipment.weight_kg
    else:
        raise ValueError(f"unknown carrier: {carrier}")
