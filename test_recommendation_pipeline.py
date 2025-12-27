from src.pipeline.recommendation_pipeline import RecommendationPipeline

if __name__ == "__main__":
    pipeline = RecommendationPipeline()
    final_report = pipeline.run()
    print(final_report)
