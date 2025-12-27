from src.pipeline.billing_pipeline import BillingPipeline

if __name__ == "__main__":
    pipeline = BillingPipeline()
    output = pipeline.run()
    print(f"Generated {len(output)} billing records")
    print(output)
