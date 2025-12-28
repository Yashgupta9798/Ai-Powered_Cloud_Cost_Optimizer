import yaml
import json

# from src.utils.llm_client import call_llm
from src.utils.llm_client import call_llm_full

from src.constant.paths import (
    PROJECT_PROFILE_FILE,
    BILLING_FILE,
    REPORT_FILE,
    CONFIG_DIR
)
from src.exception import CloudOptimizerException


class RecommendationEngine:
    """
    Generates cost optimization recommendations using LLM.
    """

    def _load_prompt(self) -> str:
        try:
            with open(CONFIG_DIR / "recommendation_prompt.yaml", "r", encoding="utf-8") as f:
                prompt_yaml = yaml.safe_load(f)
            return prompt_yaml["instruction"]
        except Exception as e:
            raise CloudOptimizerException("Failed to load recommendation prompt", e)

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

    def _load_existing_report(self) -> dict:
        try:
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise CloudOptimizerException("Failed to load existing cost report", e)

    def generate(self) -> dict:
        try:
            profile = self._load_project_profile()
            billing = self._load_billing()
            report = self._load_existing_report()
            analysis = report.get("analysis", {})

            services = list(analysis.get("service_costs", {}).keys())
            all_recommendations = []

            base_instruction = self._load_prompt()

            # ---- SERVICE-WISE RECOMMENDATIONS ----
            for service in services:
                prompt = f"""
    {base_instruction}

    SERVICE CATEGORY:
    {service}

    PROJECT PROFILE:
    {json.dumps(profile, indent=2)}

    COST ANALYSIS:
    {json.dumps(analysis, indent=2)}
    """
                recs = call_llm_full(prompt)

                if not isinstance(recs, list):
                    raise ValueError(f"Invalid recommendations for service: {service}")

                all_recommendations.extend(recs)

            # ---- SUMMARY GENERATION (SMALL & SAFE) ----
            with open("config/summary_prompt.yaml", "r", encoding="utf-8") as f:
                summary_instruction = yaml.safe_load(f)["instruction"]

            summary_prompt = f"""
    {summary_instruction}

    COST ANALYSIS:
    {json.dumps(analysis, indent=2)}

    RECOMMENDATIONS:
    {json.dumps(all_recommendations, indent=2)}
    """

            summary = call_llm_full(summary_prompt)

            if not isinstance(summary, dict):
                raise ValueError("Summary output must be a JSON object")

            # ---- FINAL REPORT ----
            report["recommendations"] = all_recommendations
            report["summary"] = summary

            with open(REPORT_FILE, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

            return report

        except Exception as e:
            raise CloudOptimizerException("Recommendation generation failed", e)
