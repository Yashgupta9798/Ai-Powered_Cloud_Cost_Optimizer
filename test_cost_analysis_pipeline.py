from src.pipeline.cost_analysis_pipeline import CostAnalysisPipeline

if __name__ == "__main__":
    pipeline = CostAnalysisPipeline()
    report = pipeline.run()
    print(report)
