import os
import json
from dotenv import load_dotenv
from mistralai.client import MistralClient 
from src.exception import CloudOptimizerException 
# ... other imports

load_dotenv()

try:
    MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
except KeyError:
    MISTRAL_API_KEY = None

# Initialize the client
client = MistralClient(api_key=MISTRAL_API_KEY)

MODEL_NAME = "mistral-small" # Use the cost-effective model for the free tier

def call_llm(prompt: str) -> dict | list:
    try:
        messages = [
            {"role": "user", "content": prompt}
        ]

        # ❗ NON-STREAMING CALL (CRITICAL FIX)
        response = client.chat(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.0,
            max_tokens=1200,   # allow full JSON
        )


        output_text = response.choices[0].message.content

        # --- Robust JSON extraction ---
        array_start = output_text.find("[")
        array_end = output_text.rfind("]") + 1

        if array_start != -1 and array_end != -1:
            return json.loads(output_text[array_start:array_end])

        obj_start = output_text.find("{")
        obj_end = output_text.rfind("}") + 1

        if obj_start != -1 and obj_end != -1:
            return json.loads(output_text[obj_start:obj_end])

        raise ValueError(f"No JSON found in LLM output:\n{output_text[:200]}")

    except Exception as e:
        raise CloudOptimizerException("LLM response invalid or API failed", e)


if __name__ == "__main__":
    prompt = """
Return ONLY valid JSON.
No explanation.

{
  "test": "success"
}
"""
    print(call_llm(prompt))