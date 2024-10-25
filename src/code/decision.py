import marimo

__generated_with = "0.7.5"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __():
    class Var:
        def __init__(self, name: str, desc: str, value: any):
            self.name = name
            self.desc = desc
            if not callable(value):
                self.value = lambda: value
            else:
                self.value = value

        def __repr__(self) -> str:
            return f"Var({self.name}={self.value})"

        def __add__(self, other):
            if not isinstance(other, Var):
                raise TypeError(f"Operand must be of type Var, instead got {other}")

            return Var(
                f"{self.name}+{other.name}",
                "sum",
                lambda: self.value() + other.value()
            )

        def __sub__(self, other):
            if not isinstance(other, Var):
                raise TypeError(f"Operand must be of type Var, instead got {other}")

            return Var(
                f"{self.name}-{other.name}",
                "difference",
                lambda: self.value() - other.value()
            )

        def __mul__(self, other):
            if not isinstance(other, Var):
                raise TypeError(f"Operand must be of type Var, instead got {other}")

            return Var(
                f"{self.name}*{other.name}",
                "product",
                lambda: self.value() * other.value()
            )

        def __truediv__(self, other):
            if not isinstance(other, Var):
                raise TypeError(f"Operand must be of type Var, instead got {other}")

            return Var(
                f"{self.name}/{other.name}",
                "quotient",
                lambda: self.value() / other.value()
            )
    return Var,


@app.cell
def __(Var):
    class Param(Var):
        def __init__(self, name: str, desc: str, value: any):
            super().__init__(name, desc, value)


    return Param,


@app.cell
def __(Var):
    class Output(Var):
        def __init__(self, name: str, desc: str, value: any):
            super().__init__(name, desc, value)

        def simulate(n: int = 10000):
            pass
    return Output,


@app.cell
def __(Param, np):
    total = (
        Param("trips", "number of trips", lambda: np.random.poisson(5))
        * Param("cost", "cost per trip", 385)
    )
    total.value()
    return total,


@app.cell
def __(total):
    for i in range(10):
        print(total.value())
    return i,


@app.cell
def __():
    import numpy as np
    import matplotlib.pyplot as plt

    plt.hist(np.random.poisson(10, 1000))
    plt.show()
    return np, plt


@app.cell
def __(Param, np):
    # Car buying v/s renting decision

    car_price = Param("price", "price of car", 20_50_000) # 12.5 lakh INR
    depreciation = car_price * Param("total dep", "dep", 0.25)

    trips_per_year = Param(
        "trips_per_year", "avg trips per month",
        lambda: np.random.poisson(36)
    )
    num_years = Param("years", "number of years", 2)

    cost_per_trip = depreciation / (trips_per_year * num_years)
    cost_per_trip.value()
    return car_price, cost_per_trip, depreciation, num_years, trips_per_year


@app.cell
def __(cost_per_trip, np, plt):
    # Create an array of 10000 samples of cost_per_trip
    samples = np.array([cost_per_trip.value() for _ in range(10000)])

    # Plot a histogram of the samples
    plt.figure(figsize=(10, 6))
    plt.hist(samples, bins=50, edgecolor='black')
    plt.title('Distribution of Cost per Trip')
    plt.xlabel('Cost per Trip (INR)')
    plt.ylabel('Frequency')
    plt.show()

    # Calculate and print some statistics
    print(f"Mean cost per trip: {np.mean(samples):.2f} INR")
    print(f"Median cost per trip: {np.median(samples):.2f} INR")
    print(f"Standard deviation: {np.std(samples):.2f} INR")
    print(f"5th percentile: {np.percentile(samples, 5):.2f} INR")
    print(f"95th percentile: {np.percentile(samples, 95):.2f} INR")

    return samples,


@app.cell
def __(np, samples, stats):
    # Calculate the 95% confidence interval from samples
    confidence_level = 0.95
    sample_mean = np.mean(samples)
    sample_std = np.std(samples, ddof=1)  # ddof=1 for sample standard deviation
    sample_size = len(samples)

    # Calculate the margin of error
    margin_of_error = stats.t.ppf((1 + confidence_level) / 2, df=sample_size-1) * (sample_std / np.sqrt(sample_size))

    # Calculate the confidence interval
    ci_lower = sample_mean - margin_of_error
    ci_upper = sample_mean + margin_of_error

    print(f"95% Confidence Interval: ({ci_lower:.2f}, {ci_upper:.2f}) INR")

    return (
        ci_lower,
        ci_upper,
        confidence_level,
        margin_of_error,
        sample_mean,
        sample_size,
        sample_std,
    )


if __name__ == "__main__":
    app.run()
