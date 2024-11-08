import marimo

__generated_with = "0.7.5"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    IMAGE_SIZE = (16, 16)
    return IMAGE_SIZE, mo, np, plt


@app.cell
def __():
    Shape = list[tuple[int, int]]
    # Offsets for the S shape, starting at top left
    # %%
    #  %%
    S_OFFSETS = [(0, 0), (0, 1), (1, 1), (1, 2)]

    # Offsets for the L shape, starting at top left
    # %
    # %
    # %%
    L_OFFSETS = [(0, 0), (1, 0), (2, 0), (2, 1)]
    return L_OFFSETS, S_OFFSETS, Shape


@app.cell
def __(IMAGE_SIZE, Shape, np):
    def draw_shape(s: Shape):
        img = np.zeros(IMAGE_SIZE)

        # Pick a random starting point
        start_x = np.random.randint(IMAGE_SIZE[0] - 4)
        start_y = np.random.randint(IMAGE_SIZE[1] - 4)
        for offset in s:
            img[start_x + offset[0], start_y + offset[1]] = np.random.normal(0.75, 0.2)
        return img
    return draw_shape,


@app.cell
def __(S_OFFSETS, draw_shape, plt):
    plt.imshow(draw_shape(S_OFFSETS), cmap="grey")
    return


@app.cell
def __(plt):
    def show(shape):
        plt.imshow(shape, cmap="grey")
        plt.show()
    return show,


@app.cell
def __(S_OFFSETS, draw_shape, np):
    # create a numpy array of shape (N, 16, 16) made up of N images
    N = 8192
    TRAINING = np.array([draw_shape(S_OFFSETS) for _ in range(N)])
    return N, TRAINING


@app.cell
def __(TRAINING, show):
    show(TRAINING[6])
    return


if __name__ == "__main__":
    app.run()
