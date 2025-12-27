import json

from src.components.cost_analyzer import CostAnalyzer
from src.constant.paths import REPORT_FILE
from src.exception import CloudOptimizerException


class CostAnalysisPipeline:
    def run(self) -> dict:
        try:
            analyzer = CostAnalyzer()
            analysis = analyzer.analyze()

            # Initialize report with analysis only (recommendations added in STEP 11)
            report = {
                "analysis": analysis
            }

            with open(REPORT_FILE, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

            return report

        except Exception as e:
            raise CloudOptimizerException("Cost analysis pipeline execution failed", e)
