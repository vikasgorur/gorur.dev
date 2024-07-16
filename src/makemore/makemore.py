import marimo

__generated_with = "0.6.3"
app = marimo.App(width="full", app_title="Building Makemore")


@app.cell
def __():
    import pandas as pd


    def read_movie_names() -> list[str]:
        movies = pd.read_csv("src/makemore/movies.csv")
        return [
            n.lower()
            for n in list(movies.query("Language == 'hindi'")["Movie Name"])
        ]


    def has_special_chars(name: str) -> bool:
        AZ = set("abcdefghijklmnopqrstuvwxyz ")
        return len(set(name) - AZ) > 0


    def clean_names(names: list[str]) -> list[str]:
        return [n for n in names if not has_special_chars(n)]


    NAMES = clean_names(read_movie_names())
    return NAMES, clean_names, has_special_chars, pd, read_movie_names


@app.cell
def __(NAMES):
    N_TOKENS = len(set(c.lower() for name in NAMES for c in name)) + 1
    print(f"Loaded {len(NAMES)} movie names, n_tokens = {N_TOKENS}")
    return N_TOKENS,


@app.cell
def __():
    import torch


    def stoi(s: str) -> int:
        assert len(s) == 1
        if s == " ":
            return 26
        elif s == ".":
            return 27
        else:
            return ord(s) - ord("a")


    def itos(i: int) -> str:
        if i == 27:
            return "."
        elif i == 26:
            return " "
        else:
            return chr(i + ord("a"))


    assert itos(stoi("f")) == "f"
    assert itos(stoi(".")) == "."
    assert itos(stoi(" ")) == " "
    return itos, stoi, torch


@app.cell
def __(N_TOKENS, torch):
    from dataclasses import dataclass


    @dataclass
    class BigramModel:
        probs: torch.tensor


    def bigram_uniform_model() -> BigramModel:
        return BigramModel(probs=torch.full((N_TOKENS, N_TOKENS), 1.0 / N_TOKENS))


    UNIFORM = bigram_uniform_model()
    return BigramModel, UNIFORM, bigram_uniform_model, dataclass


@app.cell
def __(BigramModel, NAMES, N_TOKENS, stoi, torch):
    def bigram_counts_model() -> BigramModel:
        counts = torch.zeros((N_TOKENS, N_TOKENS))
        for name in NAMES:
            name = "." + name + "."
            for c, c_next in zip(name, name[1:]):
                counts[stoi(c), stoi(c_next)] += 1

        # Normalize the counts into probabilities on each row
        probs = counts / counts.sum(1, keepdim=True)
        return BigramModel(probs)
    return bigram_counts_model,


@app.cell
def __(bigram_counts_model):
    FREQUENCY = bigram_counts_model()
    return FREQUENCY,


@app.cell
def __(FREQUENCY):
    import matplotlib.pyplot as plt

    plt.imshow(FREQUENCY.probs)
    return plt,


@app.cell
def __(FREQUENCY, itos, stoi, torch):
    def sample(model, token: str) -> str:
        return itos(
            torch.multinomial(
                model.probs[stoi(token), :], replacement=True, num_samples=1
            )
        )


    sample(FREQUENCY, "q  ")
    return sample,


@app.cell
def __(FREQUENCY, sample):
    def generate_names(model, n: int) -> list[str]:
        names = []
        for i in range(n):
            result = ""
            token = "."
            for i in range(10):
                next_token = sample(model, token)
                if next_token == ".":
                    break

                result += next_token

            names.append(result)
        return names


    generate_names(FREQUENCY, 1)
    return generate_names,


@app.cell
def __(N_TOKENS):
    import math

    -math.log(1 / N_TOKENS, 2)
    return math,


if __name__ == "__main__":
    app.run()
