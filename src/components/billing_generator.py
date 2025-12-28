import yaml
import json
from pathlib import Path

# from src.utils.llm_client import call_llm
from src.utils.llm_client import call_llm_full

from src.constant.paths import PROJECT_PROFILE_FILE, BILLING_FILE
from src.exception import CloudOptimizerException


class SyntheticBillingGenerator:
    """
    Generates synthetic cloud billing data using LLM.
    """

    def __init__(self, prompt_path: Path):
        self.prompt_path = prompt_path

    def _load_prompt_template(self) -> str:
        try:
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                prompt_yaml = yaml.safe_load(f)
            return prompt_yaml["instruction"]
        except Exception as e:
            raise CloudOptimizerException("Failed to load billing prompt template", e)

    def _load_project_profile(self) -> dict:
        try:
            with open(PROJECT_PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise CloudOptimizerException("Failed to read project profile file", e)

    def generate(self) -> list:
        try:
            instruction = self._load_prompt_template()
            project_profile = self._load_project_profile()

            services = [
                "Compute",
                "Database",
                "Storage",
                "Networking",
                "Monitoring"
            ]

            all_records = []

            for service in services:
                prompt = f"""
    {instruction}

    SERVICE CATEGORY:
    {service}

    PROJECT PROFILE:
    {json.dumps(project_profile, indent=2)}

    REMEMBER:
    - Generate ONLY 2–3 records
    - Output JSON ARRAY ONLY
    """
                records = call_llm_full(prompt)

                if not isinstance(records, list):
                    raise ValueError(f"Invalid billing output for service: {service}")

                all_records.extend(records)

            # Save final merged billing
            with open(BILLING_FILE, "w", encoding="utf-8") as f:
                json.dump(all_records, f, indent=2)

            return all_records

        except Exception as e:
            raise CloudOptimizerException("Synthetic billing generation failed", e)

