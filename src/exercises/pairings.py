import numpy as np
import itertools

def main():
    total = 0
    pairings = set()
    for p in itertools.permutations(range(4)):
        print(f"adding {(p[0], p[1])} {(p[2], p[3])}")
        pairings.add(frozenset({(p[0], p[1]), (p[2], p[3])}))

    print(pairings)

if __name__ == "__main__":
    main()
