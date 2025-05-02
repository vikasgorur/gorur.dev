import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { dot, sigmoid, vectorAdd, randomVector } from "./autoencoder";

describe("Vector primitives", () => {
  it("computes dot product correctly", () => {
    expect(dot([1, 2, 3], [1, 2, 3])).toBe(14);
  });

  it("computes sigmoid correctly", () => {
    expect(sigmoid([-1, 0, 1])).toEqual(
        [0.2689414213699951, 0.5, 0.7310585786300049]
    );
  });

  it("computes sums correctly", () => {
    expect(vectorAdd([-1, 0, 1], [1, 0, -1])).toEqual(
        [0, 0, 0]
    );
  });

  it("generates a random vector of the right size", () => {
    expect(randomVector(10).length).toBe(10);
  });
});
