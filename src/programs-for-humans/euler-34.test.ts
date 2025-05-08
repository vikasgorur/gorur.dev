import { describe, it, expect } from "vitest";
import { isDigitFactorial } from "./euler-34";

describe("isDigitFactorial", () => {
    it("should return true for numbers that are sum of their digits factorials", () => {
        expect(isDigitFactorial(145)).toBe(true); // 1! + 4! + 5! = 1 + 24 + 120 = 145
    });

    it("should return false for numbers that are not sum of their digits factorials", () => {
        expect(isDigitFactorial(123)).toBe(false);
        expect(isDigitFactorial(100)).toBe(false);
    });

    it("should handle single digit numbers correctly", () => {
        expect(isDigitFactorial(1)).toBe(true); // 1! = 1
        expect(isDigitFactorial(2)).toBe(true); // 2! = 2
    });

    it("should return false for 0", () => {
        expect(isDigitFactorial(0)).toBe(false);
    });
}); 