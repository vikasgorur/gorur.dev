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


if __name__ == "__main__":
    app.run()
