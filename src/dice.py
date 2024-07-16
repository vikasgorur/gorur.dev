import marimo

__generated_with = "0.6.3"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    from collections import defaultdict


    def roll_dice(n: int) -> np.array:
        counts = defaultdict(lambda: 0)
        for i in range(n):
            total = np.random.randint(1, 7) - np.random.randint(1, 7)
            counts[total] += 1

        return np.array([counts[k] for k in sorted(counts.keys())])


    N = 100000
    rolls = roll_dice(N)
    return N, defaultdict, mo, np, roll_dice, rolls


@app.cell
def __(rolls):
    import matplotlib.pyplot as plt

    plt.bar(range(2, 13), rolls)
    return plt,


@app.cell
def __(N, rolls):
    # Normalize rolls and print probabilities
    print(rolls / N * 100)
    return


@app.cell
def __(N, defaultdict, np):
    def roll_flat_dice(n: int) -> np.array:
        counts = defaultdict(lambda: 0)
        for i in range(n):
            d1 = np.random.choice([6, 6, 6, 0, 0, 0])
            d2 = np.random.choice([6, 5, 4, 3, 2, 1])
            total = d1 + d2
            counts[total] += 1

        return np.array([counts[k] for k in sorted(counts.keys())])


    flat_rolls = roll_flat_dice(N)
    return flat_rolls, roll_flat_dice


@app.cell
def __(flat_rolls, plt):
    plt.bar(range(1, 13), flat_rolls)
    return


if __name__ == "__main__":
    app.run()
