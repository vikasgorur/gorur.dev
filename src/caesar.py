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
                return chr((ord(c) + n) % 26 + ord("A"))


    def caesar_encrypt(s: str, n: int) -> str:
        return "".join([rot(c, n) for c in s])


    def caesar_decrypt(s: str, n: int) -> str:
        return "".join([rot(c, -n) for c in s])


    caesar_encrypt("VIKAS", 9)
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
def __(letter_pmf):
    HOLMES = letter_pmf(open("/Users/vikasprasad/hobby/cryptopals/holmes.txt").read())
    return HOLMES,


@app.cell
def __(letter_pmf):
    GETTYSBURG = letter_pmf("""Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.

    Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.

    But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth.""")
    return GETTYSBURG,


if __name__ == "__main__":
    app.run()
