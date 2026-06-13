// Shared model. Real money wants integer cents; number keeps these teaching
// examples short. LineItem is plain readonly data (a value object): two fields,
// no behavior, and right that way — there is nothing to guard.

export interface LineItem {
  readonly name: string;
  readonly price: number;
}
