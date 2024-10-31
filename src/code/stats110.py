import marimo

__generated_with = "0.7.5"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __():
    import itertools

    players = range(8)

    all_pairings = set()
    for p in itertools.permutations(players):
        division = set(p[:4])
        opponents = set(players) - division
        all_pairings.update({(w, b) for w in division for b in opponents})

    print(len(all_pairings))
    return all_pairings, division, itertools, opponents, p, players


@app.cell
def __(math):
    math.comb(4, 2) * 2 * 2
    return


@app.cell
def __(math):
    math.comb(8, 4) * math.factorial(4)
    return


@app.cell
def __():
    import math
    math.comb(20, 10) * math.factorial(10)

    return math,


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
