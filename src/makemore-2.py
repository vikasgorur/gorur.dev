

import marimo

__generated_with = "0.13.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    return (pd,)


@app.cell
def _(pd):
    def read_movie_names() -> list[str]:
        movies = pd.read_csv("src/data/movies.csv")

        def has_special_chars(name: str) -> bool:
            AZ = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")
            return len(set(name) - AZ) > 0

        return [
            n.upper()
            for n in list(movies.query("Language == 'hindi'")["Movie Name"])
            if not has_special_chars(n.upper())
        ]

    MOVIES = read_movie_names()
    MOVIES[1000:1005]
    return (MOVIES,)


@app.function
def stoi(s: str) -> int:
    assert len(s) == 1
    if s == ".":
        return 27
    elif s == " ":
        return 26
    else:
        return ord(s) - ord("A")


@app.function
def itos(i: int) -> str:
    if i == 27:
        return "."
    elif i == 26:
        return " "
    else:
        return chr(i + ord("A"))


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Training set

        For the input to the neural network we'll do one-hot encoding of each token.
        """
    )
    return


@app.cell
def _():
    import torch
    import torch.nn.functional as F
    import matplotlib.pyplot as plt

    xenc = F.one_hot(torch.tensor([stoi(t) for t in 'SHOLAY']), num_classes=28).float()
    plt.imshow(xenc)
    return torch, xenc


@app.cell
def _():
    return


@app.cell
def _(torch, xenc):
    W = torch.randn((28, 28))
    xenc @ W
    return


@app.cell
def _(torch):
    def train():
        W = torch.randn((28, 28))
    return


@app.cell
def _(model, torch):
    def sample(model: torch.tensor, context: str) -> str:
        return itos(
            torch.multinomial(
                model[stoi(context), :],
                replacement=True,
                num_samples=1
            )
        )

    print(sample(model, '.'))
    return (sample,)


@app.cell
def _(model, sample, torch):
    def generate(model: torch.tensor, n: int) -> list[str]:
        names = []
        for i in range(n):
            result = ""
            token = "."
            while True:
                token = sample(model, token)
                if token == '.':
                    break

                result += token

            names.append(result)
        return names

    generate(model, 5)
    return


@app.cell
def _(model):
    import math

    def nll(name: str) -> float:
        logprobs = 0
        for c, c_next in zip(name, name[1:]):
            logprobs += math.log(model[stoi(c)][stoi(c_next)])

        return -logprobs

    nll('SHOLAY')
    return (nll,)


@app.cell
def _(MOVIES, nll):
    LOSS = sum([nll(name) for name in MOVIES]) / len(MOVIES)
    LOSS
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
