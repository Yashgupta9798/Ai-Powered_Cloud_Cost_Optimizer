from pathlib import Path

from src.components.profile_extractor import ProjectProfileExtractor
from src.constant.paths import CONFIG_DIR
from src.exception import CloudOptimizerException


class ProfilePipeline:
    def __init__(self):
        self.prompt_path = CONFIG_DIR / "profile_prompt.yaml"

    def run(self) -> dict:
        try:
            extractor = ProjectProfileExtractor(self.prompt_path)
            return extractor.extract()
        except Exception as e:
            raise CloudOptimizerException("Profile pipeline execution failed", e)
