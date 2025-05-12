import { describe, it, expect } from "vitest";
import { fac, choose } from "./euler-15";

describe("fac", () => {
    it("computes factorial correctly", () => {
        expect(fac(7n)).toEqual(5040n);
        expect(fac(12n)).toEqual(479001600n);
    });
    it("computes n choose k correctly", () => {
        expect(choose(10n, 5n)).toEqual(252n);
    });
});
