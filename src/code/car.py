import marimo

__generated_with = "0.11.29"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np

    from chances import Spread, DiscreteUniform, Var, plot_distribution
    return DiscreteUniform, Spread, Var, mo, np, plot_distribution


@app.cell
def _():
    # https://www.sbigeneral.in/blog/motor-insurance/motor-decoding-insurance/what-is-car-depreciation-and-how-it-works
    SCHEDULE = [0.0, 0.15, 0.2, 0.3, 0.4, 0.5]
    return (SCHEDULE,)


@app.cell
def _(np):
    class Discrete:
        def __init__(self, density: dict[float, float]):
            self.values = list(density.keys())
            self.probs = [density[v] for v in self.values]

        def __call__(self, n=1):
            return np.random.choice(self.values, size=n, p=self.probs)
    return (Discrete,)


@app.cell
def _(Discrete):
    TRIPS_D = Discrete({
            1.0: 0.5,
            2.0: 0.25,
            3.0: 0.25
        })
    return (TRIPS_D,)


@app.cell
def _():
    PARAMETERS = {
        "fuel_per_trip": 200,
        "yearly_maintenance": 10_000,
        "yearly_insurance": 50_000,
        "cost_of_car": 21_00_000,
    }
    return (PARAMETERS,)


@app.cell
def _(PARAMETERS):
    N_TRIPS_VALUES = [1.0, 2.0, 3.0]
    N_TRIPS_P = [0.5, 0.25, 0.25]

    def simulate_week() -> float:
        "Simulate a week and return the number of trips and cost incurred"
        trips_in_week = 7.0 #np.random.choice(N_TRIPS_VALUES, 1, p=N_TRIPS_P)

        return trips_in_week, PARAMETERS["fuel_per_trip"] * trips_in_week

    return N_TRIPS_P, N_TRIPS_VALUES, simulate_week


@app.cell
def _(simulate_week):
    simulate_week()
    return


@app.cell
def _(PARAMETERS, SCHEDULE):
    PARAMETERS["cost_of_car"] * SCHEDULE[2]
    return


@app.cell
def _(PARAMETERS, SCHEDULE, simulate_week):
    def simulate_years(years):
        total_trips_cost = 0
        n_trips = 0

        for _ in range(0, 52*years):
            n, c = simulate_week()
            total_trips_cost += c
            n_trips += n

        insurance = years * PARAMETERS["yearly_insurance"]
        maintenance = years * PARAMETERS["yearly_maintenance"]

        cost_of_trips = (
            insurance +
            maintenance +
            total_trips_cost +
            PARAMETERS["cost_of_car"] * SCHEDULE[years]
        )

        return cost_of_trips / n_trips
    return (simulate_years,)


@app.cell
def _(np, simulate_years):
    import matplotlib.pyplot as plt

    def plot_output(years):
        samples = np.array([simulate_years(years) for _ in range(10001)])

        # Calculate percentiles
        p5, p95 = np.percentile(samples, [5, 95])
        mean = np.mean(samples)

        # Plot a histogram of the samples
        plt.figure(figsize=(10, 6))
        plt.hist(samples, bins=50, edgecolor='black')

        # Add vertical lines for percentiles
        plt.axvline(x=p5, color='r', linestyle='--', label=f'p5 = {p5:.2f}')
        plt.axvline(x=mean, color='g', linestyle='--', label=f'Mean = {mean:.2f}')
        plt.axvline(x=p95, color='r', linestyle='--', label=f'p95 = {p95:.2f}')

        plt.title(f"Cost per trip ({years} years ownership)")
        plt.xlabel("Cost per trip")
        plt.ylabel('Count')
        plt.legend()
        plt.show()
    return plot_output, plt


@app.cell
def _(plot_output):
    plot_output(2)
    return


@app.cell(disabled=True)
def _(plot_output):
    import cProfile
    import pstats
    from io import StringIO

    # Create a Profile object
    pr = cProfile.Profile()

    # Run the function with profiling
    pr.enable()
    plot_output(2)
    pr.disable()

    # Create a StringIO object to capture the output
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()

    # Print the profiling results
    print(s.getvalue())
    return StringIO, cProfile, pr, ps, pstats, s


@app.cell(disabled=True)
def _(np, plt, simulate_years):
    def plot_years():
        yearly = []
        for y in range(1, 5):
            yearly.append(np.array([simulate_years(y) for _ in range(10000)]))

        yearly = np.array(yearly)  # Transpose the data

        plt.figure(figsize=(10, 6))
        bp = plt.boxplot(yearly, labels=['Year 1', 'Year 2', 'Year 3', 'Year 4'], showfliers=False)
        plt.ylim(bottom=0)
        plt.title('Cost per Trip Distribution by Year')
        plt.xlabel('Year')
        plt.ylabel('Cost per Trip (INR)')
        plt.grid(True)

        for i, year_data in enumerate(yearly.T):
            mean_value = np.mean(year_data)
            plt.text(i + 1, mean_value, f'{mean_value:.0f}', 
                     horizontalalignment='center', verticalalignment='bottom')

        plt.show()

    plot_years()
    return (plot_years,)


if __name__ == "__main__":
    app.run()
