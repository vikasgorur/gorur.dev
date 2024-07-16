import marimo

__generated_with = "0.6.3"
app = marimo.App(app_title="")


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        rf"""
        David MacKay, *Information Theory, Inference and Learning Algorithms*, 2003.

        ## Exercise 2.4

        An urn contains $K$ balls, of which $B$ are black and $W = K - B$ are white. Fred draws a ball at random from the urn and replaces it, $N$ times.

        (a) What is the probability distribution of the number of times a black ball is drawn, $n_B$?

        (b) What is the expectation of $n_B$? What is the variance of $n_B$? What is the standard deviation of $n_B$? Give numerical answers for the cases $N = 5$ and $N = 400$, when $B = 2$ and $K = 10$.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        ## Answer

        $$ p = \frac{B}{K}$$

        $$n_B = {N \choose n} p^n (1-p)^{(N-n)}$$
        """
    )
    return


@app.cell
def __():
    import marimo as mo
    import matplotlib.pyplot as plt
    import math

    B = 2.0
    K = 10.0
    N = 400


    def pnb(n: int) -> float:
        p = B / K
        return math.comb(N, n) * p**n * (1 - p) ** (N - n)


    plt.plot(range(N + 1), [pnb(i) for i in range(N + 1)])
    return B, K, N, math, mo, plt, pnb


@app.cell
def __(B, K, N, mo):
    def expect_nb(N: int):
        return (B / K) * N


    mo.md(f"$E[n_B]$ = {expect_nb(N)}")
    return expect_nb,


@app.cell
def __(B, K, N, mo):
    def var_nb():
        return (B / K) ** 2 * N - ((B / K) * N) ** 2


    mo.md(f"$var(n_B)$ = {var_nb()}")
    return var_nb,


@app.cell
def __():
    def stddev_nb():
        pass
    return stddev_nb,


if __name__ == "__main__":
    app.run()
