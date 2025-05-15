import { BitSet } from "bitset";

export function sieveOfEratosthenes(N: number): Array<number> {
    let sieve = new BitSet();
    sieve.setRange(2, N);

    for (let x = 2; x <= Math.floor(Math.sqrt(N)); x++) {
        for (let i = 2; i <= Math.ceil(N/x); i++) {
            sieve.clear(x * i);
        }
    }

    let primes = [];
    for (let i = 2; i <= N; i++) {
        if (sieve.get(i)) primes.push(i);
    }
    return primes
}

export function primeDivisors(n: number, primes: Array<number>): Array<number> {
    let divisors = [];
    for (let p of primes) {
        if (n % p === 0) divisors.push(p);
        if (p > n) break; 
    }
    return divisors;
}

// Problem 47

// Given that p divides n, find the max p^k that divides n
export function maxPrimePower(n: number, p: number): number {
    let k = 2;
    while (n % Math.pow(p, k) === 0) {
        k++;
    }
    return Math.pow(p, k-1);
}

export function primePowerFactors(n: number, primes: Array<number>): Array<number> {
    return primeDivisors(n, primes).map((d, _) => maxPrimePower(n, d));
}

// Returns true if all the factors of a sequence of numbers are
// all distinct
export function allDistinct(seqFactors: Array<Array<number>>): boolean {
    const allFactors = seqFactors.flat();
    const factorSet = new Set<number>(allFactors);

    return allFactors.length === factorSet.size;
}

export function problem47() {
    console.time('problem47');
    let low = 10;
    const primes = sieveOfEratosthenes(1000000);
    let seq = [
        primePowerFactors(10, primes),
        primePowerFactors(11, primes),
        primePowerFactors(12, primes),
        primePowerFactors(13, primes),
    ];
    
    const allAtleastFour = (seq: Array<Array<number>>) => seq.flat().length >= 16;
    while (!(allDistinct(seq) && allAtleastFour(seq))) {
        seq.shift();
        seq.push(primePowerFactors(low + 4, primes));
        low++;
    }
    console.timeEnd('problem47');
    console.log(`(${low}: ${seq[0]}) (${low+1}: ${seq[1]}) (${low+2}: ${seq[2]}) (${low+3}: ${seq[3]})`);
}

//problem47();

export function isGoldbachExpressible(
    n: number, primes: Array<number>
): boolean {

    const isEven = (x: number) => x % 2 === 0;
    const isSquare = (x: number) => Math.sqrt(x) === Math.floor(Math.sqrt(x));

    for (let p of primes) {
        const rest = n - p;
        if (isEven(rest) && isSquare(rest/2)) {
            return true;
        }
        if (p > n) break; 
    }
    return false;
}

function problem46() {
    let n = 3;
    const LIMIT = 100000;
    const primes = sieveOfEratosthenes(LIMIT);

    while (n < LIMIT) {
        if (!isGoldbachExpressible(n, primes)) {
            console.log(n);
            break;
        }
        n += 2;
    }
}

problem46();