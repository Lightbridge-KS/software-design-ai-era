// Observer — canonical conceptual example. Run: npx tsx conceptObserver.ts
//
// A Subject maintains a list of observers and notifies each on change.
// Observers subscribe without the Subject knowing their concrete types.

export type Observer = (event: string) => void;

export class Subject {
  private readonly observers: Observer[] = [];
  subscribe(observer: Observer): void {
    this.observers.push(observer);
  }
  notify(event: string): void {
    for (const observer of this.observers) observer(event);
  }
}

// Demo
const subject = new Subject();
subject.subscribe((e) => console.log(`A saw ${e}`));
subject.subscribe((e) => console.log(`B saw ${e}`));
subject.notify("ping"); // A saw ping / B saw ping
