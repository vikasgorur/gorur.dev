import marimo

__generated_with = "0.6.3"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import pandas as pd

    candidates = pd.read_csv("src/data/candidates.csv")
    candidates
    return candidates, mo, np, pd


@app.cell
def __(candidates):
    PLAYERS = {p: i for i, p in enumerate(sorted(set(candidates["white_player"])))}
    INDEXES = {i: p for i, p in enumerate(sorted(set(candidates["white_player"])))}


    def ptoi(p: str) -> int:
        return PLAYERS[p]


    def itop(i: int) -> str:
        return INDEXES[i]
    return INDEXES, PLAYERS, itop, ptoi


@app.cell
def __(PLAYERS, candidates, np, pd, ptoi):
    def results_matrix(df: pd.DataFrame) -> np.array:
        "Convert the results DF into a nxn matrix of scores"

        N = len(PLAYERS.keys())
        results = np.zeros((N, N))

        for i, row in df.iterrows():
            results[ptoi(row["white_player"]), ptoi(row["black_player"])] += row["white_points"]
            results[ptoi(row["black_player"]), ptoi(row["white_player"])] += row["black_points"]

        return results


    A = results_matrix(candidates)
    A
    return A, results_matrix


@app.cell
def __(PLAYERS, candidates, pd, ptoi, results_matrix):
    def player_scores(df: pd.DataFrame) -> dict[str, float]:
        # For each player, store their index in a dict
        A = results_matrix(df)

        scores = {}
        for name in PLAYERS.keys():
            scores[name] = A[ptoi(name)].sum()

        return scores


    player_scores(candidates)
    return player_scores,


@app.cell
def __(A, np):
    # solve the matrix equation Ax = lambda x
    l, v = np.linalg.eig(A)
    l
    return l, v


@app.cell
def __(A, np):
    A @ np.random.random(8)
    return


@app.cell
def __(A, np):
    def power(A: np.array, n: int) -> np.array:
        v = np.random.random(A.shape[0])
        for i in range(n):
            Av = A @ v
            v = Av / np.linalg.norm(Av)
        return v


    power(A, 32)
    return power,


@app.cell
def __(itop, v):
    q = v[:, 0]
    quality = {}
    for i, q_ in enumerate(q):
        quality[itop(i)] = q_

    # Sort by values
    quality
    return i, q, q_, quality


@app.cell
def __():
    N = 5
    B = 2.0
    K = 10.0

    import math


    def pn(n):
        "prob. that black is drawn n times"
        return math.comb(N, n) * (B / K) ** n * (1 - B / K) ** (N - n)


    N*(B/K)
    return B, K, N, math, pn


if __name__ == "__main__":
    app.run()
