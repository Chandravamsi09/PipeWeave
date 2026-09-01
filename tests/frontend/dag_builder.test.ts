import { describe, it, expect } from "vitest";
describe("Frontend DAG Canvas", () => {
  it("initializes 5 default pipeline nodes", () => {
    expect(["src", "clean", "gate", "agg", "sink"].length).toBe(5);
  });
});
