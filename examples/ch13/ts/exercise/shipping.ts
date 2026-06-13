// Chapter 13 exercise starter: the shipping-cost tangle.
//
// Refactor with your agent using the "Strategy, right-sized" prompt from the
// chapter (adapt the names), then grade the output with the review checklist.

export interface Shipment {
  readonly weightKg: number;
  readonly destinationCountry: string;
  readonly declaredValue: number;
}

const EU = new Set(["DE", "FR", "NL"]);

export function shippingCost(shipment: Shipment, carrier: string): number {
  switch (carrier) {
    case "standard":
      return 4.9 + 0.5 * shipment.weightKg;
    case "express": {
      let base = 9.9 + 1.2 * shipment.weightKg;
      if (shipment.declaredValue > 100) base += 2.5; // mandatory insurance
      return base;
    }
    case "pickup":
      return 0;
    case "international":
      return EU.has(shipment.destinationCountry)
        ? 14.9 + 1.0 * shipment.weightKg
        : 24.9 + 2.2 * shipment.weightKg;
    default:
      throw new Error(`unknown carrier: ${carrier}`);
  }
}
