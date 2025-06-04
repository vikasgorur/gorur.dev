

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


@app.cell
def _(MOVIES):
    for i, m in enumerate(MOVIES):
        if m == 'BAAZIGAR':
            print(i, m)
    return


@app.function
def stoi(s: str) -> int:
    assert len(s) == 1
    if s == ".":
        return 27
    elif s == " ":
        return 26
    else:
        return ord(s) - ord("A")


@app.cell
def _(MOVIES):
    all_chars = sorted(list(set(''.join(MOVIES))))
    STOI = {s:i for i,s in enumerate(all_chars)}
    STOI['.'] = 27
    STOI
    return (STOI,)


@app.cell
def _(STOI):
    ITOS = {i:s for s,i in STOI.items()}
    return (ITOS,)


@app.cell
def _(MOVIES, STOI):
    import torch

    def train(corpus: list[str]) -> torch.tensor:
        N_TOKENS = 28
        counts = torch.zeros((N_TOKENS, N_TOKENS))
        for name in corpus:
            name = "." + name + "."
            for c, c_next in zip(name, name[1:]):
                counts[STOI[c], STOI[c_next]] += 1

        # Normalize the counts into probabilities on each row
        return counts / counts.sum(1, keepdim=True)

    model = train(MOVIES)
    return model, torch


@app.cell
def _(ITOS, STOI, model, torch):
    def sample(model: torch.tensor, context: str) -> str:
        return ITOS[
            torch.multinomial(
                model[STOI[context], :],
                replacement=True,
                num_samples=1
            ).item()
        ]

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
def _(MOVIES, STOI, model):
    import math

    def nll(names: list[str]) -> float:
        logprobs = 0
        count = 0
        for name in names:
            for c, c_next in zip(name, name[1:]):
                logprobs += math.log(model[STOI[c]][STOI[c_next]])
                count += 1

        return -logprobs / count

    nll(MOVIES)
    return


@app.cell
def _(MOVIES, STOI, torch):
    def training_set() -> (torch.Tensor, torch.Tensor):
        xs, ys = [], []
        for name in MOVIES:
            chars = ['.'] + list(name) + ['.']
            for c1, c2 in zip(chars, chars[1:]):
                ix1 = STOI[c1]
                ix2 = STOI[c2]
                xs.append(ix1)
                ys.append(ix2)
    
        return (torch.tensor(xs), torch.tensor(ys))
        
    return (training_set,)


@app.cell
def _(training_set):
    X, Y = training_set()
    print(X.shape, Y.shape)
    return X, Y


@app.cell
def _(X, Y, torch):
    import torch.nn.functional as F

    def train_nn() -> torch.Tensor:
        W = torch.randn((28, 28), requires_grad=True)
        N = len(X)
        for k in range(100):
            X_enc = F.one_hot(X, num_classes=28).float()
            logits = X_enc @ W
            counts = logits.exp()
            probs = counts / counts.sum(1, keepdims=True)
            #print(probs.shape)
            loss = -probs[torch.arange(N), Y].log().mean() + 0.01*(W**2).mean()
            print(loss.item())

            W.grad = None
            loss.backward()

            W.data += -50 * W.grad

    return (train_nn,)


@app.cell
def _(train_nn):
    train_nn()
    return


if __name__ == "__main__":
    app.run()
