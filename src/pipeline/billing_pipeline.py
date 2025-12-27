from pathlib import Path

from src.components.billing_generator import SyntheticBillingGenerator
from src.constant.paths import CONFIG_DIR
from src.exception import CloudOptimizerException


class BillingPipeline:
    def __init__(self):
        self.prompt_path = CONFIG_DIR / "billing_prompt.yaml"

    def run(self) -> list:
        try:
            generator = SyntheticBillingGenerator(self.prompt_path)
            return generator.generate()
        except Exception as e:
            raise CloudOptimizerException("Billing pipeline execution failed", e)
