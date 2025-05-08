import BitSet from "bitset";

export function digitSet(n: number): BitSet {
    const bs = new BitSet("0000000000");
    const DIGITS: Record<string, number> = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    };
    for (const c of n.toString()) {
        bs.set(DIGITS[c]);
    }
    return bs;
}

export function allEqual(sets: Array<BitSet>): boolean {
    const first = sets[0];
    for (let i = 1; i < sets.length; i++) {
        if (!first.equals(sets[i])) {
            return false;
        }
    }
    return true;
}

export function tryNumber(n: number): boolean {
    const sets: Array<BitSet> = [1, 2, 3, 4, 5, 6].map((x) => digitSet(n * x));
    return allEqual(sets);
}

function problem52() {
    console.time("problem52");
    for (let n = 1; n < 1000000; n++) {
        if (tryNumber(n)) {
            const vals = [1, 2, 3, 4, 5, 6].map((x) => n * x);
            console.log(`${vals.join(" ")}`);
        }
    }
    console.timeEnd("problem52");
}

problem52();
