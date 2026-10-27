import json
from pathlib import Path
from src.data_loader import load_data
from src.analyzer import analyse_resource
from src.investigator import investigate_cause
from src.visualizer import (
    plot_consumption,
    plot_occupancy_vs_consumption,
    plot_equipment_hours,
    show_correlation_analysis
)


PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def print_report(result, investigation):
    resource = result["resource"].upper()
    unit = (
        "litres/day"
        if result["resource"] == "water"
        else "kWh/day"
    )

    print("\n" + "=" * 65)
    print(f"{resource} INVESTIGATION REPORT")
    print("=" * 65)
    print(f"Date: {result['date']}")
    print(
        f"Expected consumption: "
        f"{result['expected_usage']:.2f} {unit}"
    )

    print(
        f"Actual consumption: "
        f"{result['actual_usage']:.2f} {unit}"
    )

    print(
        f"Percentage deviation: "
        f"{result['percentage_change']:+.2f}%"
    )

    print(
        f"Statistical threshold: "
        f"{result['anomaly_threshold']:.2f} {unit}"
    )

    print(
        f"Historical standard deviation: "
        f"{result['standard_deviation']:.2f}"
    )

    print(
        f"Historical minimum: "
        f"{result['historical_minimum']:.2f} {unit}"
    )

    print(
        f"Historical maximum: "
        f"{result['historical_maximum']:.2f} {unit}"
    )

    print(f"Trend: {result['trend']}")

    print(f"Severity: {result['severity']}")

    print(
        f"Anomaly detected: "
        f"{result['anomaly_detected']}"
    )

    print("\nPossible explanations:")

    for cause in investigation["possible_causes"]:

        print(f"- {cause}")

    print("\nRecommended actions:")

    for recommendation in investigation["recommendations"]:

        print(f"- {recommendation}")

    print("\nConfidence and limitations:")

    print(investigation["confidence"])

    print("=" * 65)


def save_report(result, investigation):

    report = {
        "analysis": result,
        "investigation": investigation
    }

    filename = (
        f"{result['resource']}_"
        f"{result['date']}_report.json"
    )

    report_path = REPORTS_DIR / filename

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print(f"\nReport saved to: {report_path}")


def main():
    print("\n")
    print("*" * 65)
    print(" AI WATER AND ENERGY WASTE INVESTIGATOR")
    print(" Version 3: NumPy + Pandas")
    print("*" * 65)
    try:
        #Load the dataset.
        df = load_data()

        print("\nDataset loaded successfully.")
        print(f"Total records: {len(df)}")
        print("\nAvailable resources:")
        print(
            df.groupby("resource").size().to_string()
        )

        while True:
            print("\nChoose an option:")
            print("1. Analyse water")
            print("2. Analyse electricity")
            print("3. Analyse both")
            print("4. View dataset summary")
            print("5. Visualize water consumption")
            print("6. Visualize electricity consumption")
            print("7. Compare occupancy and water consumption")
            print("8. Compare occupancy and electricity consumption")
            print("9. Compare equipment hours and electricity consumption")
            print("10. View correlation analysis")
            print("11. Exit")
            
            choice = input("\nEnter your choice: ").strip()
            if choice == "1":
                resources = ["water"]
            elif choice == "2":
                resources = ["electricity"]
            elif choice == "3":
                resources = ["water", "electricity"]
            elif choice == "4":
                print("\nDataset summary:")
                print(df.describe(include="all").to_string())
                print("\nAverage consumption by resource:")
                print(
                    df.groupby("resource")["consumption"]
                    .mean()
                    .to_string()
                )

                continue
            elif choice == "5":
                plot_consumption(df, "water")
                continue
            elif choice == "6":
                plot_consumption(df, "electricity")
                continue
            elif choice == "7":
                plot_occupancy_vs_consumption(df, "water")
                continue
            elif choice == "8":
                plot_occupancy_vs_consumption(df, "electricity")
                continue
            elif choice == "9":
                plot_equipment_hours(df)
                continue
            elif choice == "10":
                show_correlation_analysis(df)
                continue
            elif choice == "11":
                print("Application closed.")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 11.")
                continue

            for resource in resources:
                try:
                    result = analyse_resource(df, resource)
                    investigation = investigate_cause(result)
                    print_report(result, investigation)
                    save_report(result, investigation)
                    
                except ValueError as error:
                    print(f"Could not analyse {resource}: {error}")
                    
    except (FileNotFoundError, ValueError) as error:
            print(f"\nApplication error: {error}")


if __name__ == "__main__":
    main()