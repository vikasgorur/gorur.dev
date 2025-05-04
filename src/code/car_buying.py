

import marimo

__generated_with = "0.13.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    import pandas as pd
    return np, pd


@app.cell
def _(np, pd):
    # For binomial distribution with n=7 and mean=2, p = mean/n = 2/7
    df = pd.DataFrame()
    df['trips_per_week'] = np.random.binomial(n=8, p=2/8, size=1000)  # Generate 1000 samples
    return (df,)


@app.cell
def _(df):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))

    # Calculate value counts and normalize to get probabilities
    value_counts = df['trips_per_week'].value_counts(normalize=True).sort_index()

    # Create line plot
    plt.plot(value_counts.index, value_counts.values, marker='o', linestyle='-', linewidth=2)

    plt.title('Probability Distribution of Trips per Week')
    plt.xlabel('Trips per Week')
    plt.ylabel('Probability')
    plt.grid(alpha=0.3)

    # Add text annotations for probabilities
    for x, y in zip(value_counts.index, value_counts.values):
        plt.text(x, y, f'{y:.3f}', ha='center', va='bottom')

    # Set x-axis ticks to whole numbers
    plt.xticks(range(0, 9))

    plt.gca()
    return


@app.cell
def _(np):
    from dataclasses import dataclass

    @dataclass
    class ModelParams:
        cost_of_car: float
        fuel_per_trip: float
        yearly_maintenance: float
        yearly_insurance: float
        depreciation: list[float]

    @dataclass
    class ModelOutput:
        cost_per_trip: dict[int, np.array]
    return (ModelParams,)


@app.cell
def _(ModelParams):
    PARAMS = ModelParams(
        cost_of_car=21_00_000,
        fuel_per_trip=200,
        yearly_maintenance=10_000,
        yearly_insurance=50_000,
        depreciation=[0.0, 0.15, 0.2, 0.3, 0.4, 0.5]
    )
    return (PARAMS,)


@app.cell
def _(ModelParams, np):
    def simulate_timeline(years: int, params: ModelParams) -> float:
       # Simulate trips
       total_weeks = years * 52
       trips = np.sum(np.random.binomial(n=8, p=2/8, size=total_weeks))
   
       # Total cost of trips
       insurance = years * params.yearly_insurance
       maintenance = years * params.yearly_maintenance
       depreciation = params.cost_of_car * params.depreciation[years]
   
       total_cost = (
           trips * params.fuel_per_trip
           + insurance
           + maintenance
           + depreciation
       )

       return total_cost / trips
   
    return (simulate_timeline,)


@app.cell
def _(PARAMS, simulate_timeline):
    simulate_timeline(1, PARAMS)
    return


if __name__ == "__main__":
    app.run()
