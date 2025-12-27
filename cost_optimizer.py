import json
import os

from src.pipeline.profile_pipeline import ProfilePipeline
from src.pipeline.billing_pipeline import BillingPipeline
from src.pipeline.cost_analysis_pipeline import CostAnalysisPipeline
from src.pipeline.recommendation_pipeline import RecommendationPipeline
from src.constant.paths import (
    PROJECT_DESC_FILE,
    PROJECT_PROFILE_FILE,
    BILLING_FILE,
    REPORT_FILE
)
from src.exception import CloudOptimizerException


def print_menu():
    print("\n==== AI-Powered Cloud Cost Optimizer ====")
    print("1. Enter new project description")
    print("2. Run Complete Cost Analysis")
    print("3. View Recommendations")
    print("4. Export Report")
    print("5. Exit")


def enter_project_description():
    print("\nEnter project description (end with an empty line):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    description = "\n".join(lines)

    with open(PROJECT_DESC_FILE, "w", encoding="utf-8") as f:
        f.write(description)

    print("\n✔ Project description saved.")

    # Run profile extraction immediately
    ProfilePipeline().run()
    print("✔ Project profile generated.")


def run_complete_analysis():
    print("\nRunning complete cost analysis pipeline...\n")

    BillingPipeline().run()
    print("✔ Synthetic billing generated.")

    CostAnalysisPipeline().run()
    print("✔ Cost analysis completed.")

    RecommendationPipeline().run()
    print("✔ Cost optimization recommendations generated.")

    print("\n🎉 Complete analysis finished successfully.")


def view_recommendations():
    if not os.path.exists(REPORT_FILE):
        print("\n❌ No report found. Run cost analysis first.")
        return

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        report = json.load(f)

    recommendations = report.get("recommendations", [])

    if not recommendations:
        print("\n❌ No recommendations available.")
        return

    print("\n==== COST OPTIMIZATION RECOMMENDATIONS ====\n")
    for idx, rec in enumerate(recommendations, 1):
        print(f"{idx}. {rec['title']}")
        print(f"   Service: {rec['service']}")
        print(f"   Potential Savings: ₹{rec['potential_savings']}")
        print(f"   Effort: {rec['implementation_effort']} | Risk: {rec['risk_level']}")
        print(f"   Providers: {', '.join(rec['cloud_providers'])}")
        print("")


def export_report():
    if not os.path.exists(REPORT_FILE):
        print("\n❌ No report found to export.")
        return

    export_path = input("\nEnter export file name (e.g. final_report.json): ").strip()

    with open(REPORT_FILE, "r", encoding="utf-8") as src:
        data = src.read()

    with open(export_path, "w", encoding="utf-8") as dest:
        dest.write(data)

    print(f"\n✔ Report exported to {export_path}")


def main():
    while True:
        try:
            print_menu()
            choice = input("\nSelect an option (1–5): ").strip()

            if choice == "1":
                enter_project_description()
            elif choice == "2":
                run_complete_analysis()
            elif choice == "3":
                view_recommendations()
            elif choice == "4":
                export_report()
            elif choice == "5":
                print("\nExiting. Goodbye!")
                break
            else:
                print("\n❌ Invalid choice. Please select 1–5.")

        except CloudOptimizerException as e:
            print(f"\n❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break


if __name__ == "__main__":
    main()
