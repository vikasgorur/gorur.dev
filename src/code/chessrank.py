import marimo

__generated_with = "0.7.5"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import pandas as pd
    from pprint import pprint
    import matplotlib.pyplot as plt

    candidates = pd.read_csv("src/data/candidates.csv")
    candidates
    return candidates, mo, np, pd, plt, pprint


@app.cell
def __(candidates):
    PTOI = {p: i for i, p in enumerate(sorted(set(candidates["white_player"])))}
    ITOP = {i: p for i, p in enumerate(sorted(set(candidates["white_player"])))}
    return ITOP, PTOI


@app.cell
def __(PTOI, candidates, np, pd):
    def results_matrix(df: pd.DataFrame) -> np.array:
        "Convert the results DF into a nxn matrix of scores"

        N = len(PTOI.keys())
        results = np.zeros((N, N))

        for i, row in df.iterrows():
            results[PTOI[row["white_player"]], PTOI[row["black_player"]]] += row["white_points"]
            results[PTOI[row["black_player"]], PTOI[row["white_player"]]] += row["black_points"]

        return results


    A = results_matrix(candidates)
    A
    return A, results_matrix


@app.cell
def __(PTOI, candidates, pd, pprint, results_matrix):
    def player_scores(df: pd.DataFrame) -> dict[str, float]:
        # For each player, store their index in a dict
        A = results_matrix(df)

        scores = {}
        for name in PTOI.keys():
            scores[name] = A[PTOI[name]].sum()

        return scores


    pprint(sorted(player_scores(candidates).items(), key=lambda item: item[1], reverse=True))
    return player_scores,


@app.cell
def __(A, np):
    # solve the matrix equation Ax = lambda x
    E = np.linalg.eig(A)
    E.eigenvectors
    return E,


@app.cell
def __(A, np):
    A @ np.random.random(8)
    return


@app.cell
def __(np):
    def power_iters(A: np.array, n: int) -> list[np.array]:
        np.random.seed(64)
        v = np.random.random(A.shape[0])
        vectors = [v]
        for i in range(n):
            Av = A @ v
            v = Av / np.linalg.norm(Av)
            vectors.append(v)
        return vectors
    return power_iters,


@app.cell
def __(ITOP, np):
    def ranking(q: np.array) -> list[str]:
        return [
            f"{name:<8}{score*1000:.0f}"
            for name, score in sorted([(ITOP[i], q_) for i, q_ in enumerate(q)], key=lambda x: x[1], reverse=True)
        ]
    return ranking,


@app.cell
def __(A, power_iters):
    qq = power_iters(A, 8)[7]
    return qq,


@app.cell
def __(plt, qq, ranking):
    fig, ax = plt.subplots(figsize=(4, 8)) # width, height
    ax.axis("off")

    # Get the ranking text
    ranks = ranking(qq)

    # Display text, one line per player
    y_pos = 0
    for rank in ranks:
        ax.text(0.1, 0.9 - (y_pos / len(ranks)) * 0.3, rank, fontsize=12, fontfamily="JetBrains Mono")
        y_pos += 1

    plt.gcf()
    return ax, fig, rank, ranks, y_pos


@app.cell
def __(ranks):
    ranks
    return


if __name__ == "__main__":
    app.run()
