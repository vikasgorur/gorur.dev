import { describe, it, expect, beforeAll } from "vitest";
import { decrypt, gibberishScore } from "./euler-59";

function stringToCharCodes(s: string): number[] {
    return Array.from(s).map(char => char.charCodeAt(0));
}

describe("Problem 59", () => {
    it("computes gibberishScore correctly", () => {
        expect(gibberishScore(stringToCharCodes("abc%"))).toBe(0.25);
        expect(gibberishScore(stringToCharCodes("foo"))).toBe(0);
        expect(gibberishScore(stringToCharCodes("%^&"))).toBe(1);
    });
    it("decrypts using key XOR", () => {
        expect(decrypt([0, 0, 0], [1, 2, 3])).toEqual([1, 2, 3]);
        expect(decrypt([1, 1, 1], [1, 1, 1])).toEqual([0, 0, 0]);
        expect(() => decrypt([1, 1, 1], [1, 1])).toThrow();
    });
});
