import marimo

__generated_with = "0.10.17"
app = marimo.App(width="medium", css_file="marimo.css")


@app.cell
def _():
    import marimo as mo

    import numpy as np
    import pandas as pd

    np.random.seed(43)
    return mo, np, pd


@app.cell
def _(mo):
    mo.md("""## General methods""")
    return


@app.cell
def _(np, wifi):
    def split_dataset(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        n = data.shape[0]

        split = int(n * 0.85)
        indices = np.random.permutation(n)
        train_idx, test_idx = indices[:split], indices[split:]
        return data[train_idx], data[test_idx]

    train_wifi, test_wifi = split_dataset(wifi)
    return split_dataset, test_wifi, train_wifi


@app.cell
def _(np):
    def knn(data: np.ndarray, x: np.ndarray, k: int) -> int:
        assert data.shape[1] == x.shape[0] + 1
        distances = np.apply_along_axis(
            lambda r: np.hstack([
                np.linalg.norm(r[:-1] - x, ord=2),
                r[-1]
            ]),
            1, #axis
            data
        )
        ranked = distances[np.argsort(distances[:, 0])]
        top_k = ranked[:k]
        top_k_labels = top_k[:, -1]
        return np.bincount(top_k_labels.astype(int)).argmax()
    return (knn,)


@app.cell
def _(knn, np):
    def predict(train: np.ndarray, test: np.ndarray, k=9) -> np.ndarray:
        return np.apply_along_axis(
            lambda r: np.hstack([
                r[:-1], # data point
                r[-1],  # actual
                knn(train, r[:-1], k) # predicted
            ]),
            1, # axis: apply to reach row
            test
        )
    return (predict,)


@app.cell
def _(np):
    def score(predictions: np.ndarray) -> float:
        return (
            # number of rows where last two columns are same
            sum(predictions[:, -2] == predictions[:, -1])
            # total number of rows
            / predictions.shape[0]
        )
    return (score,)


@app.cell
def _(mo):
    mo.md(r"""## Wifi dataset""")
    return


@app.cell
def _(np, pd):
    def load_wifi() -> np.ndarray:
        wifi = pd.read_csv(
            "src/data/wifi.tsv",
            sep="\t",
            header=None,
            names=["ap1", "ap2", "ap3", "ap4", "ap5", "ap6", "ap7", "room"]
        )
        wifi = wifi.query("room == 1 or room == 2")[["ap5", "ap7", "room"]]
        return wifi.to_numpy()

    wifi = load_wifi()
    return load_wifi, wifi


@app.cell
def _(predict, score, test_wifi, train_wifi):
    predicted_wifi = predict(train_wifi, test_wifi)
    score(predicted_wifi)
    return (predicted_wifi,)


@app.cell
def _(train_wifi):
    import matplotlib.pyplot as plt

    # Create the scatter plot
    plt.figure(figsize=(8, 6))

    # Split data by room label (third column)
    room1_mask = train_wifi[:, -1] == 1
    room2_mask = train_wifi[:, -1] == 2

    # Plot points for each room with different colors
    plt.scatter(train_wifi[room1_mask, 0], train_wifi[room1_mask, 1], 
               color='red', label='Room 1', alpha=0.6)
    plt.scatter(train_wifi[room2_mask, 0], train_wifi[room2_mask, 1], 
               color='blue', label='Room 2', alpha=0.6)

    plt.xlabel('AP5 Signal Strength')
    plt.ylabel('AP7 Signal Strength')
    plt.title('WiFi Signal Strengths by Room')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    return plt, room1_mask, room2_mask


@app.cell
def _(mo):
    mo.md(r"""## Recipes""")
    return


@app.cell
def _(mo):
    mo.md(r"""### Loader""")
    return


@app.cell
def _(pd):
    raw = pd.read_json("src/code/data/cooking_train.json")
    df = raw.query("cuisine == 'italian' or cuisine == 'indian'")
    df = df.reset_index(drop=True)
    df
    return df, raw


@app.cell
def _(BagOfWordsEncoder, np, pd):
    def load_recipes(encoder_class):
        raw = pd.read_json("src/code/data/cooking_train.json")
        # filter for only two cuisines to make the algo work
        df = raw.query("cuisine == 'italian' or cuisine == 'indian'").reset_index(drop=True)

        cuisine_labels = {}
        for i, c in enumerate(set(df["cuisine"])):
            cuisine_labels[c] = i

        enc = encoder_class(df["ingredients"])
        data = np.zeros((len(df), enc.ndims + 1))

        for i, row in df.iterrows():
            data[i] = np.append(
                enc.encode(row["ingredients"]),
                cuisine_labels[row["cuisine"]]
            )

        return data, cuisine_labels

    recipes, cuisine_labels = load_recipes(BagOfWordsEncoder)
    return cuisine_labels, load_recipes, recipes


@app.cell
def _(cuisine_labels):
    cuisine_labels
    return


@app.cell
def _(mo):
    mo.md("""### Bag of words""")
    return


@app.cell
def _(np):
    class BagOfWordsEncoder:
        def __init__(self, sentences):
            # map each word to an index in the vector
            self.words = dict()

            for s in sentences:
                for ingredient in s:
                    for word in ingredient.split(" "):
                        if word not in self.words:
                            self.words[word] = len(self.words)

            self.ndims = len(self.words)

        def encode(self, sentence):
            v = np.zeros(len(self.words))
            for w in sentence:
                if w in self.words:
                    v[self.words[w]] = 1

            return v
    return (BagOfWordsEncoder,)


@app.cell
def _(recipes, split_dataset):
    recipes_train, recipes_test = split_dataset(recipes)
    print(recipes_train.shape)
    print(recipes_test.shape)
    return recipes_test, recipes_train


@app.cell
def _(np):
    def sample_test_data(X: np.ndarray, n: int):
        indices = np.random.choice(X.shape[0], size=n, replace=False)
        return X[indices]

    #recipes_test_sample = sample_test_data(recipes_test, 100)
    return (sample_test_data,)


@app.cell
def _(predict, recipes_test, recipes_train, score):
    predicted_recipes = predict(recipes_train, recipes_test, k=7)
    score(predicted_recipes)
    return (predicted_recipes,)


@app.cell
def _(mo):
    mo.md(r"""### Word2vec""")
    return


@app.cell
def _(np):
    import gensim.downloader as gd

    class Word2VecEncoder:
        def __init__(self, sentences):
            self.model = gd.load("word2vec-google-news-300")
            self.ndims = self.model.vector_size

        def encode(self, sentence):
            vectors = [self.model[word] for word in sentence if word in self.model]
            if not vectors:  # If no words were found in the model
                return np.zeros(self.ndims)  # Return zero vector
            return np.mean(vectors, axis=0)
    return Word2VecEncoder, gd


@app.cell
def _(Word2VecEncoder):
    word2vec = Word2VecEncoder(None)
    return (word2vec,)


@app.cell
def _(word2vec):
    word2vec.encode(["garlic", "salt"]).shape
    return


@app.cell
def _(Word2VecEncoder, load_recipes):
    recipes_2, cuisine_labels_2 = load_recipes(Word2VecEncoder)
    return cuisine_labels_2, recipes_2


@app.cell
def _(predict, recipes_2, score, split_dataset):
    recipes_2_train, recipes_2_test = split_dataset(recipes_2)
    #recipes_2_test_sample = sample_test_data(recipes_2_test, 200)

    predicted_recipes_2 = predict(recipes_2_train, recipes_2_test, k=23)
    score(predicted_recipes_2)


    return predicted_recipes_2, recipes_2_test, recipes_2_train


@app.cell
def _(predict, recipes_2_test, recipes_2_train, score):
    ks = range(3, 29, 2)
    scores = [score(predict(recipes_2_train, recipes_2_test, k=k)) for k in ks]


    return ks, scores


@app.cell
def _(ks, plt, scores):
        
    plt.figure(figsize=(10, 6))
    plt.plot(ks, scores, marker='o')
    plt.xlabel('k (number of neighbors)')
    plt.ylabel('Accuracy Score')
    plt.title('KNN Performance with Different k Values')
    plt.grid(True, alpha=0.3)
    plt.show()
    return


if __name__ == "__main__":
    app.run()
