function fac(n: bigint): bigint {
    let result = 1n;
    for (let i: bigint = n; i > 1n; i--) {
        result *= i;
    }
    return result;
}

const choose = (n: bigint, k: bigint): bigint => fac(n) / (fac(k) * fac(n - k));

/**
 * This problem can be reduced to (k = 20)
 *
 * Distribute k unlabeled balls into k+1 labeled urns, where any
 * urn can be empty.
 */
function problem15() {
    console.log(choose(40n, 20n));
}

export { fac, choose };

problem15();
