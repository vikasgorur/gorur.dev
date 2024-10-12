import marimo

__generated_with = "0.7.5"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __():
    def rot(c: str, n: int) -> str:
        "Rotate the character c by n places, wrapping around. c must be an uppercase letter"
        assert ord("A") <= ord(c) <= ord("Z") or c == " "
        match c:
            case " ":
                return c
            case _:
                return chr((ord(c) - ord("A") + n) % 26 + ord("A"))


    def caesar_encrypt(s: str, n: int) -> str:
        return "".join([rot(c, n) for c in s])


    def caesar_decrypt(s: str, n: int) -> str:
        return "".join([rot(c, -n) for c in s])


    caesar_encrypt("VWXYZ", 5)
    return caesar_decrypt, caesar_encrypt, rot


@app.cell
def __():
    from collections import Counter


    def letter_pmf(s: str) -> dict[str, float]:
        s = s.upper()
        counts = Counter(s)
        total = sum(counts.values())
        return {c: counts[c] / total for c in counts.keys()}
    return Counter, letter_pmf


@app.cell
def __():
    import math


    def kl_divergence(p: dict[str, float], q: dict[str, float]):
        return sum(p[x] * (math.log2(p[x]) - math.log2(q[x])) for x in p.keys())
    return kl_divergence, math


@app.cell
def __(letter_pmf):
    HOLMES = letter_pmf(open("/Users/vikasprasad/hobby/cryptopals/holmes.txt").read())
    return HOLMES,


@app.cell
def __():
    def clean_text(s: str) -> str:
        return "".join([c for c in s if c.isalpha() or c == " "]).upper()
    return clean_text,


@app.cell
def __():
    BOOTS = """TAKE BOOTS, FOR EXAMPLE. HE EARNED THIRTY-EIGHT DOLLARS A MONTH PLUS ALLOWANCES. A REALLY GOOD PAIR OF LEATHER BOOTS COST FIFTY DOLLARS. BUT AN AFFORDABLE PAIR OF BOOTS, WHICH WERE SORT OF OKAY FOR A SEASON OR TWO AND THEN LEAKED LIKE HELL WHEN THE CARDBOARD GAVE OUT, COST ABOUT TEN DOLLARS. THOSE WERE THE KIND OF BOOTS VIMES ALWAYS BOUGHT, AND WORE UNTIL THE SOLES WERE SO THIN THAT HE COULD TELL WHERE HE WAS IN ANKH-MORPORK ON A FOGGY NIGHT BY THE FEEL OF THE COBBLES. BUT THE THING WAS THAT GOOD BOOTS LASTED FOR YEARS AND YEARS. A MAN WHO COULD AFFORD FIFTY DOLLARS HAD A PAIR OF BOOTS THAT’D STILL BE KEEPING HIS FEET DRY IN TEN YEARS’ TIME, WHILE A POOR MAN WHO COULD ONLY AFFORD CHEAP BOOTS WOULD HAVE SPENT A HUNDRED DOLLARS ON BOOTS IN THE SAME TIME AND WOULD STILL HAVE WET FEET.
    """
    return BOOTS,


@app.cell
def __(BOOTS, caesar_encrypt, clean_text):
    CIPHER = caesar_encrypt(clean_text(BOOTS), 3)
    CIPHER
    return CIPHER,


@app.cell
def __(BOOTS, HOLMES, kl_divergence, letter_pmf):
    kl_divergence(letter_pmf(BOOTS), HOLMES)
    return


@app.cell
def __(HOLMES, caesar_decrypt, kl_divergence, letter_pmf):
    import numpy as np


    def try_decrypt(cipher: str) -> (int, str):
        divergences = np.zeros(26)
        for key in range(0, 26):
            divergences[key] = kl_divergence(letter_pmf(caesar_decrypt(cipher, key)), HOLMES)

        # Find the min value key
        correct_key = np.argmin(divergences)
        return correct_key, caesar_decrypt(cipher, correct_key)
    return np, try_decrypt


@app.cell
def __(CIPHER, try_decrypt):
    try_decrypt(CIPHER)
    return


if __name__ == "__main__":
    app.run()
