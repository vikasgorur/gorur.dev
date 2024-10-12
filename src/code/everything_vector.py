import marimo

__generated_with = "0.6.3"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    import gensim.downloader as gd
    import numpy as np
    return gd, mo, np


@app.cell
def __(gd):
    model = gd.load("word2vec-google-news-300")
    return model,


@app.cell
def __(np):
    def knn(points: np.array, x: np.array, k: int) -> np.array:
        distances = np.linalg.norm(points - x, axis=1)
        return np.argsort(distances)[:k]
    return knn,


@app.cell
def __():
    from collections import Counter


    def majority(labels: list[str]) -> str:
        "Return the label that occurs the most number of times"
        return Counter(labels).most_common(1)[0][0]


    assert majority(["w1", "w2", "w1", "w3"]) == "w1"
    return Counter, majority


@app.cell
def __():
    import pandas as pd

    wifi = pd.read_csv(
        "src/data/wifi.tsv", sep="\t", header=None, names=["ap1", "ap2", "ap3", "ap4", "ap5", "ap6", "ap7", "room"]
    )

    wifi = wifi.query("room == 1 or room == 2")[["ap5", "ap7", "room"]]
    wifi
    return pd, wifi


@app.cell
def __(wifi):
    X_train = wifi.sample(frac=0.85)
    X_test = wifi.loc[~wifi.index.isin(X_train.index)]

    X_train.reset_index(inplace=True)
    X_test.reset_index(inplace=True)
    return X_test, X_train


if __name__ == "__main__":
    app.run()
