import marimo

__generated_with = "0.7.5"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return mo,


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
    Cipher = dict[str, str]

    def make_cipher(spec: list[str]) -> Cipher:
        """
        Make a cipher (a dict) from a "spec": the letters A-Z in some order
        """
        letters = [chr(ord('A') + i) for i in range(26)]
        d = {c: letters[i] for i, c in enumerate(spec)}
        d[' '] = ' '
        return d

    return Cipher, make_cipher


@app.cell
def __(Cipher, make_cipher):
    import random

    CIPHER = make_cipher(list("QWERTYUIOPASDFGHJKLZXCVBNM"))

    def encrypt(cipher: Cipher, s: str) -> str:
        return "".join([cipher[c] for c in s.upper()])

    return CIPHER, encrypt, random


@app.cell
def __(letter_pmf):
    def clean_text(s: str) -> str:
        return "".join([c for c in s if c.isalpha() or c == " "]).upper()

    HOLMES = letter_pmf(clean_text(open("src/data/holmes.txt").read()))
    return HOLMES, clean_text


@app.cell
def __(LetterPmf):
    import math

    def relative_entropy(p: LetterPmf, q: LetterPmf) -> float:
        return sum(p[x] * (math.log2(p[x]) - math.log2(q[x]))
                   for x in p.keys())
    return math, relative_entropy


@app.cell
def __(Cipher, random):
    def random_swap(c: Cipher) -> Cipher:
        def random_letter() -> str:
            return chr(ord('A') + random.randint(0, 25))
        
        c_ = c.copy()
        for i in range(10):
            a = random_letter()
            b = random_letter()
            c_[a], c_[b] = c_[b], c_[a]

        return c_
    return random_swap,


@app.cell
def __(CIPHER, clean_text, encrypt):
    CTEXT = encrypt(CIPHER, clean_text("""
    Friends, Romans, countrymen, lend me your ears;
    I come to bury Caesar, not to praise him.
    The evil that men do lives after them;
    The good is oft interred with their bones;
    So let it be with Caesar. The noble Brutus
    Hath told you Caesar was ambitious:
    If it were so, it was a grievous fault,
    And grievously hath Caesar answer’d it.
    Here, under leave of Brutus and the rest–
    For Brutus is an honourable man;
    So are they all, all honourable men–
    Come I to speak in Caesar’s funeral.
    He was my friend, faithful and just to me:
    But Brutus says he was ambitious;
    And Brutus is an honourable man.
    He hath brought many captives home to Rome
    Whose ransoms did the general coffers fill:
    Did this in Caesar seem ambitious?
    When that the poor have cried, Caesar hath wept:
    Ambition should be made of sterner stuff:
    Yet Brutus says he was ambitious;
    And Brutus is an honourable man.
    You all did see that on the Lupercal
    I thrice presented him a kingly crown,
    Which he did thrice refuse: was this ambition?
    Yet Brutus says he was ambitious;
    And, sure, he is an honourable man.
    I speak not to disprove what Brutus spoke,
    But here I am to speak what I do know.
    You all did love him once, not without cause:
    What cause withholds you then, to mourn for him?
    O judgment! thou art fled to brutish beasts,
    And men have lost their reason. Bear with me;
    My heart is in the coffin there with Caesar,
    And I must pause till it come back to me.
    """))
    return CTEXT,


@app.cell
def __(CIPHER, CTEXT, Cipher):
    def decrypt(cipher: Cipher, s: str) -> str:
        inverse = {v: k for k, v in cipher.items()}
        return "".join([inverse[c] for c in s.upper()])

    decrypt(CIPHER, CTEXT)
    return decrypt,


@app.cell
def __(Cipher, make_cipher, random):
    def random_cipher() -> Cipher:
        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(letters)
        return make_cipher(letters)

    return random_cipher,


@app.cell
def __(
    CTEXT,
    HOLMES,
    decrypt,
    letter_pmf,
    random_cipher,
    random_swap,
    relative_entropy,
):
    def try_decrypt(secret: str) -> None:
        c = random_cipher()
        for i in range(1000):
            loss = relative_entropy(letter_pmf(decrypt(c, secret)), HOLMES)
            c_new = random_swap(c)
            loss_new = relative_entropy(letter_pmf(decrypt(c_new, secret)), HOLMES)
            if loss_new < loss:
                c = c_new

            if i % 100 == 0:
                print(f"iter = {i}, loss = {loss}")
                print(decrypt(c, secret))

    try_decrypt(CTEXT)
    return try_decrypt,


if __name__ == "__main__":
    app.run()
