import yaml
import json
from pathlib import Path

# from src.utils.llm_client import call_llm
from src.utils.llm_client import call_llm_stream

from src.constant.paths import PROJECT_DESC_FILE, PROJECT_PROFILE_FILE
from src.exception import CloudOptimizerException


class ProjectProfileExtractor:
    """
    Extracts a structured project profile from free-form text using LLM.
    """

    def __init__(self, prompt_path: Path):
        self.prompt_path = prompt_path

    def _load_prompt_template(self) -> str:
        try:
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                prompt_yaml = yaml.safe_load(f)
            return prompt_yaml["instruction"]
        except Exception as e:
            raise CloudOptimizerException("Failed to load profile prompt template", e)

    def _load_project_description(self) -> str:
        try:
            with open(PROJECT_DESC_FILE, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise CloudOptimizerException("Failed to read project description file", e)

    def extract(self) -> dict:
        try:
            instruction = self._load_prompt_template()
            description = self._load_project_description()

            final_prompt = f"""
{instruction}

PROJECT DESCRIPTION:
{description}
"""

            profile_json = call_llm_stream(final_prompt)

            # Save output
            with open(PROJECT_PROFILE_FILE, "w", encoding="utf-8") as f:
                json.dump(profile_json, f, indent=2)

            return profile_json

        except Exception as e:
            raise CloudOptimizerException("Project profile extraction failed", e)
