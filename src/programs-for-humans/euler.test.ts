import { describe, it, expect, beforeAll } from 'vitest';
import { allDistinct, maxPrimePower, primeDivisors, primePowerFactors, sieveOfEratosthenes } from './euler';

let primes: number[];

describe('Problem 47', () => {
    beforeAll(() => {
        primes = sieveOfEratosthenes(1000);
    });
    it('should return array of primes under N', () => {
        expect(sieveOfEratosthenes(20)).toEqual([2, 3, 5, 7, 11, 13, 17, 19]);
    });
    it("should return the prime divisors of a number", () => {
        expect(primeDivisors(15, primes)).toEqual([3, 5])
    });
    it("should return the max prime power factor of a number", () => {
        expect(maxPrimePower(644, 2)).toBe(4);
        expect(maxPrimePower(21, 7)).toBe(7);
    });
    it("should return prime power factors of a number", () => {
        expect(primePowerFactors(644, primes)).toEqual([4, 7, 23]);
        expect(primePowerFactors(645, primes)).toEqual([3, 5, 43]);
    });
    it("should check if all factors of a sequence of numbers are distinct", () => {
        expect(allDistinct([
            primePowerFactors(14, primes), 
            primePowerFactors(15, primes)
        ])).toBeTruthy()
    });
});