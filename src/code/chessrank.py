import marimo

__generated_with = "0.9.23"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import pandas as pd
    from pprint import pprint
    import matplotlib.pyplot as plt

    candidates = pd.read_csv("data/candidates.csv")
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
def __(PTOI, candidates, pd, results_matrix):
    def player_scores(df: pd.DataFrame) -> pd.DataFrame:
        A = results_matrix(df)
        scores = {}
        for name in PTOI.keys():
            scores[name] = [A[PTOI[name]].sum()]

        # Convert dictionary to DataFrame
        scores_df = pd.DataFrame.from_dict(
            scores, orient="index", columns=["Score"]
        )
        # Sort by score in descending order
        scores_df = scores_df.sort_values('Score', ascending=False)

        return scores_df

    scores = player_scores(candidates)
    scores
    return player_scores, scores


@app.cell
def __(A, np):
    # solve the matrix equation Ax = lambda x
    E = np.linalg.eig(A)
    E.eigenvectors
    return (E,)


@app.cell
def __(A, np):
    A @ np.random.random(8)
    return


@app.cell
def __(np):
    def power_iters(A: np.array, n: int) -> list[np.array]:
        np.random.seed(12)
        v = np.random.random(A.shape[0])
        vectors = [v]
        for i in range(n):
            Av = A @ v
            v = Av / np.linalg.norm(Av)
            vectors.append(v)
        return vectors
    return (power_iters,)


@app.cell
def __(ITOP, np):
    def ranking(q: np.array) -> list[str]:
        return sorted([(ITOP[i], q_) for i, q_ in enumerate(q)], key=lambda x: x[1], reverse=True)
    return (ranking,)


@app.cell
def __():
    def rank_changes(
        prev_ranking: list[tuple[str, float]], 
        curr_ranking: list[tuple[str, float]]
    ) -> dict[str, int]:
        # Create maps of name -> position for both rankings
        prev_positions = {name: i for i, (name, _) in enumerate(prev_ranking)}
        curr_positions = {name: i for i, (name, _) in enumerate(curr_ranking)}

        # For each player, compute how many positions they moved
        # (previous position - current position, so positive means they improved)
        changes = {name: prev_positions[name] - curr_positions[name] 
                  for name in prev_positions.keys()}

        return changes
    return (rank_changes,)


@app.cell
def __(A, plt, power_iters, rank_changes, ranking):
    num_iters = 8  # Increased to show 8 plots total
    fig, axes = plt.subplots(2, 4, figsize=(4*4, 8))  # 2 rows, 4 columns
    axes = axes.flatten()  # Flatten to 1D array for easier indexing

    prev_ranks = None
    for i, q in enumerate(power_iters(A, num_iters-1)):
        # Get the ranking tuples
        ranks = ranking(q)
        changes = {}
        if prev_ranks:
            changes = rank_changes(prev_ranks, ranks)
        # Turn off axes for this subplot
        axes[i].axis('off')

        prev_ranks = ranks
        # Display text, one line per player
        y_pos = 0
        for name, score in ranks:
            delta = changes.get(name, 0)
            prefix = ""
            if delta < 0:
                prefix = "↓"
                color = "red"
            elif delta > 0:
                prefix = "↑"
                color = "green"
            else:
                color = "black"


            line = f"{prefix:<2} {name:<10}{score*1000:.0f}"
            axes[i].text(
                0.1,
                0.9 - (y_pos / len(ranks)) * 0.7,
                line,
                fontsize=12,
                fontname='Menlo',
                color=color
            )
            axes[i].text(
                0.5,
                0.05,
                f"iter {i}",
                fontsize=10,
                fontname="Menlo",
                ha='center'
            )

            y_pos += 1

    plt.gcf()
    return (
        axes,
        changes,
        color,
        delta,
        fig,
        i,
        line,
        name,
        num_iters,
        prefix,
        prev_ranks,
        q,
        ranks,
        score,
        y_pos,
    )


@app.cell
def __(ranks):
    ranks
    return


if __name__ == "__main__":
    app.run()
