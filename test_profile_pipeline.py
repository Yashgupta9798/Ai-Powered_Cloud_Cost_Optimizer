from src.pipeline.profile_pipeline import ProfilePipeline

if __name__ == "__main__":
    pipeline = ProfilePipeline()
    output = pipeline.run()
    print(output)
