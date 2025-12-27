import json
from collections import defaultdict

from src.constant.paths import PROJECT_PROFILE_FILE, BILLING_FILE, REPORT_FILE
from src.exception import CloudOptimizerException


class CostAnalyzer:
    """
    Performs deterministic cost analysis on synthetic billing data.
    """

    def _load_project_profile(self) -> dict:
        try:
            with open(PROJECT_PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise CloudOptimizerException("Failed to load project profile", e)

    def _load_billing(self) -> list:
        try:
            with open(BILLING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise CloudOptimizerException("Failed to load billing data", e)

    def analyze(self) -> dict:
        try:
            profile = self._load_project_profile()
            billing = self._load_billing()

            budget = profile.get("budget_inr_per_month", 0)

            total_cost = 0.0
            service_costs = defaultdict(float)

            for record in billing:
                cost = float(record.get("cost_inr", 0))
                service = record.get("service", "Unknown")

                total_cost += cost
                service_costs[service] += cost

            budget_variance = total_cost - budget
            is_over_budget = budget_variance > 0

            # Identify high-cost services (top contributors)
            sorted_services = dict(
                sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
            )

            high_cost_services = {
                service: cost
                for service, cost in sorted_services.items()
                if cost >= 0.2 * total_cost  # >= 20% of total cost
            }

            analysis = {
                "total_monthly_cost": round(total_cost, 2),
                "budget": budget,
                "budget_variance": round(budget_variance, 2),
                "service_costs": {k: round(v, 2) for k, v in service_costs.items()},
                "high_cost_services": {k: round(v, 2) for k, v in high_cost_services.items()},
                "is_over_budget": is_over_budget,
            }

            return analysis

        except Exception as e:
            raise CloudOptimizerException("Cost analysis failed", e)
