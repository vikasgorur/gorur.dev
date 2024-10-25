import marimo

__generated_with = "0.7.5"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __():
    import numpy as np
    import matplotlib.pyplot as plt

    IMAGE_SIZE = (16, 16)
    plt.imshow(np.random.rand(*IMAGE_SIZE), cmap='gray')
    plt.show()
    return IMAGE_SIZE, np, plt


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
def __(IMAGE_SIZE, S_OFFSETS, Shape, np, plt):
    def draw_shape(s: Shape):
        img = np.zeros(IMAGE_SIZE)

        # Pick a random starting point
        start_x = np.random.randint(IMAGE_SIZE[0] - 4)
        start_y = np.random.randint(IMAGE_SIZE[1] - 4)
        for offset in s:
            img[start_x + offset[0], start_y + offset[1]] = np.random.uniform(0.5, 1)
        return img

    plt.imshow(draw_shape(S_OFFSETS), cmap='gray')
    plt.show()
    return draw_shape,


@app.cell
def __(L_OFFSETS, draw_shape, plt):
    plt.imshow(draw_shape(L_OFFSETS), cmap='gray')
    plt.show()
    return


@app.cell
def __(S_OFFSETS, Shape, draw_shape, plt):
    # Show n examples in a grid with 8 columns
    def show_examples(n: int, shape: Shape):
        examples = [draw_shape(shape) for _ in range(n)]
        rows = (n + 7) // 8  # Calculate number of rows needed
        fig, axes = plt.subplots(rows, 8, figsize=(16, 2 * rows))
        axes = axes.flatten()  # Flatten the 2D array of axes for easier iteration
        for i, (ax, img) in enumerate(zip(axes, examples)):
            ax.imshow(img, cmap='gray')
            ax.axis('off')  # Turn off axis labels
        # Hide any unused subplots
        for j in range(i + 1, rows * 8):
            axes[j].axis('off')
            axes[j].set_visible(False)
        plt.tight_layout()
        plt.show()

    show_examples(16, S_OFFSETS)
    return show_examples,


@app.cell
def __(L_OFFSETS, show_examples):
    show_examples(16, L_OFFSETS)
    return


@app.cell
def __(S_OFFSETS, draw_shape, np):
    # A training example is represented as a structured numpy array of
    # shape (16, 16) with fields 'image' and 'label'

    example_dtype = np.dtype([('image', np.float32, (16, 16)), ('label', np.int8)])

    img = draw_shape(S_OFFSETS)
    example = np.array([(img, 1)], dtype=example_dtype)
    return example, example_dtype, img


@app.cell
def __(IMAGE_SIZE, example_dtype, np, plt):
    def blank_example():
        return np.array([(np.zeros(IMAGE_SIZE), 0)], dtype=example_dtype)

    plt.imshow(blank_example()[0]['image'], cmap='gray')
    plt.show()

    return blank_example,


@app.cell
def __(
    IMAGE_SIZE,
    S_OFFSETS,
    blank_example,
    draw_shape,
    example_dtype,
    np,
):
    def n_training_examples(n: int):
        assert n % 2 == 0
        blank = blank_example()
        neg_examples = np.array([(np.zeros(IMAGE_SIZE), 0) for _ in range(n // 2)], dtype=example_dtype)
        pos_examples = np.array([(draw_shape(S_OFFSETS), 1) for _ in range(n // 2)], dtype=example_dtype)
        examples = np.concatenate([neg_examples, pos_examples])

        np.random.shuffle(examples)
        return examples

    n_training_examples(16).shape

    return n_training_examples,


@app.cell
def __(n_training_examples):
    TRAINING = n_training_examples(16)
    TRAINING.shape
    return TRAINING,


@app.cell
def __(TRAINING):
    TRAINING[0]['label']
    return


if __name__ == "__main__":
    app.run()
