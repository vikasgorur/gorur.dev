import { describe, it, expect } from "vitest";
import { digitSet, allEqual, tryNumber } from "./euler-52";
import BitSet from "bitset";

describe("digitSet", () => {
    it("should return the digits of a number", () => {
        expect(digitSet(1234567890)).toEqual(new BitSet("1111111111"));
    });
    it("should verify that 125874 and its double have the same digits", () => {
        expect(digitSet(125874)).toEqual(digitSet(125874 * 2));
    });
    it("should verify that an array of bit sets are all equal", () => {
        expect(
            allEqual([new BitSet("0001"), new BitSet("0001"), new BitSet("0001")]),
        ).toBeTruthy();
        expect(
            allEqual([new BitSet("0001"), new BitSet("0101"), new BitSet("0001")]),
        ).toBeFalsy();
    });
    it("should verify that 52 doesn't work", () => {
        expect(tryNumber(52)).toBeFalsy();
    });
});
