// Returns true if n is the sum of the factorials of
// its digits
export function isDigitFactorial(n: number): boolean {
    const digits: string[] = [];
    const FACTORIALS: { [key: string]: number } = {
        "1": 1,
        "2": 2,
        "3": 6,
        "4": 24,
        "5": 120,
        "6": 720,
        "7": 5040,
        "8": 40320,
        "9": 362880,
    };
    digits.push(...n.toString());

    const sum = digits.reduce((total, d) => total + FACTORIALS[d], 0);
    return sum === n;
}

function problem34() {}
