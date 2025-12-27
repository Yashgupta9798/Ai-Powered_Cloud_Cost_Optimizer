from src.components.recommendation_engine import RecommendationEngine
from src.exception import CloudOptimizerException


class RecommendationPipeline:
    def run(self) -> dict:
        try:
            engine = RecommendationEngine()
            return engine.generate()
        except Exception as e:
            raise CloudOptimizerException("Recommendation pipeline execution failed", e)
