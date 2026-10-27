import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)
def plot_consumption(df, resource):

    resource_df = (
        df[df["resource"] == resource]
        .sort_values("date")
        .copy()
    )

    if len(resource_df) < 2:
        print(f"Not enough data to plot {resource}.")
        return

    # Use all readings except the latest as the baseline.
    historical = resource_df.iloc[:-1]

    expected_usage = historical["consumption"].mean()

    historical_std = historical["consumption"].std()

    actual_usage = resource_df["consumption"].iloc[-1]

    # Use the same statistical threshold as Version 3.
    threshold = max(
        expected_usage * 1.20,
        expected_usage + 2 * historical_std
    )

    # Flag observations that exceed the threshold.
    resource_df["anomaly"] = (
        resource_df["consumption"] > threshold
    )

    unit = (
        "Litres/day"
        if resource == "water"
        else "kWh/day"
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot daily consumption.
    ax.plot(
        resource_df["date"],
        resource_df["consumption"],
        marker="o",
        label="Actual Consumption"
    )

    # Plot historical expected consumption.
    ax.axhline(
        expected_usage,
        linestyle="--",
        label="Historical Average"
    )

    # Plot the statistical anomaly threshold.
    ax.axhline(
        threshold,
        linestyle=":",
        label="Anomaly Threshold"
    )

    # Highlight anomalous readings.
    anomalies = resource_df[resource_df["anomaly"]]

    if not anomalies.empty:

        ax.scatter(
            anomalies["date"],
            anomalies["consumption"],
            s=100,
            marker="x",
            label="Potential Anomaly"
        )

    ax.set_title(
        f"{resource.title()} Consumption Analysis"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel(unit)

    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.autofmt_xdate()
    fig.tight_layout()

    output_path = REPORTS_DIR / f"{resource}_consumption.png"

    fig.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    print(f"Graph saved to: {output_path}")

    plt.show()

    plt.close(fig)


def plot_occupancy_vs_consumption(df, resource):

    resource_df = (
        df[df["resource"] == resource]
        .sort_values("date")
        .copy()
    )

    if len(resource_df) < 2:
        print("Not enough data to plot occupancy.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        resource_df["occupancy"],
        resource_df["consumption"]
    )

    ax.set_title(
        f"Occupancy vs {resource.title()} Consumption"
    )

    ax.set_xlabel("Occupancy")
    ax.set_ylabel(
        "Consumption (litres/day)"
        if resource == "water"
        else "Consumption (kWh/day)"
    )

    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    output_path = (
        REPORTS_DIR /
        f"{resource}_occupancy_comparison.png"
    )

    fig.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    print(f"Graph saved to: {output_path}")

    plt.show()

    plt.close(fig)


def plot_equipment_hours(df):

    electricity_df = (
        df[df["resource"] == "electricity"]
        .sort_values("date")
        .copy()
    )

    if electricity_df.empty:
        print("No electricity data available.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        electricity_df["operating_hours"],
        electricity_df["consumption"]
    )

    ax.set_title(
        "Equipment Operating Hours vs Electricity Consumption"
    )

    ax.set_xlabel("Equipment Operating Hours")
    ax.set_ylabel("Electricity Consumption (kWh/day)")

    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    output_path = (
        REPORTS_DIR / "equipment_hours_vs_electricity.png"
    )

    fig.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    print(f"Graph saved to: {output_path}")

    plt.show()

    plt.close(fig)


def show_correlation_analysis(df):

    numerical_columns = [
        "consumption",
        "occupancy",
        "temperature",
        "operating_hours"
    ]

    print("\nCORRELATION ANALYSIS")
    print("=" * 50)

    # Analyse each resource separately because water and
    # electricity have different units and consumption scales.
    for resource in ["water", "electricity"]:

        resource_df = df[
            df["resource"] == resource
        ]

        correlation = resource_df[
            numerical_columns
        ].corr()

        print(f"\n{resource.upper()}")

        print(
            correlation.round(2).to_string()
        )

    print("\nNote:")
    print(
        "Correlation indicates association, not causation. "
        "Results from this small synthetic dataset are "
        "illustrative only."
    )

