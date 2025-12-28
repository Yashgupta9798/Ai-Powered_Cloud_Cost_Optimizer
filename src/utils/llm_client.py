import os
import json
from dotenv import load_dotenv
from mistralai.client import MistralClient

from src.exception import CloudOptimizerException

# Load env vars
load_dotenv()

# Read API key
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in environment")

# Initialize client ONCE
client = MistralClient(api_key=MISTRAL_API_KEY)

# Model name (free tier friendly)
MODEL_NAME = "mistral-tiny"


def call_llm_stream(prompt: str) -> dict:
    """
    Streaming call.
    Best for SMALL extraction-style JSON (profile extraction).
    """
    try:
        messages = [{"role": "user", "content": prompt}]

        chat_response = client.chat_stream(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.0,
            max_tokens=600,
        )

        output_text = ""
        for chunk in chat_response:
            if chunk.choices and chunk.choices[0].delta.content:
                output_text += chunk.choices[0].delta.content

        start = output_text.find("{")
        end = output_text.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError(f"No JSON object found:\n{output_text}")

        return json.loads(output_text[start:end])

    except Exception as e:
        raise CloudOptimizerException("Streaming LLM call failed", e)


def call_llm_full(prompt: str) -> dict | list:
    """
    Non-streaming call.
    Best for LARGE JSON (billing, recommendations).
    """
    try:
        messages = [{"role": "user", "content": prompt}]

        response = client.chat(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.0,
            max_tokens=1400,
        )

        output_text = response.choices[0].message.content

        # Array case
        if "[" in output_text and "]" in output_text:
            return json.loads(
                output_text[output_text.find("["): output_text.rfind("]") + 1]
            )

        # Object case
        if "{" in output_text and "}" in output_text:
            return json.loads(
                output_text[output_text.find("{"): output_text.rfind("}") + 1]
            )

        raise ValueError(f"No JSON found in output:\n{output_text}")

    except Exception as e:
        raise CloudOptimizerException("Non-streaming LLM call failed", e)



# For python test_billing_pipeline.py

# import os
# import json
# from dotenv import load_dotenv
# from mistralai.client import MistralClient 
# from src.exception import CloudOptimizerException 
# # ... other imports

# load_dotenv()

# try:
#     MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
# except KeyError:
#     MISTRAL_API_KEY = None

# # Initialize the client
# client = MistralClient(api_key=MISTRAL_API_KEY)

# MODEL_NAME = "mistral-tiny" # Use the cost-effective model for the free tier

# def call_llm(prompt: str) -> dict | list:
#     try:
#         messages = [
#             {"role": "user", "content": prompt}
#         ]

#         # ❗ NON-STREAMING CALL (CRITICAL FIX)
#         response = client.chat(
#             model=MODEL_NAME,
#             messages=messages,
#             temperature=0.0,
#             max_tokens=1200,   # allow full JSON
#         )


#         output_text = response.choices[0].message.content

#         # --- Robust JSON extraction ---
#         array_start = output_text.find("[")
#         array_end = output_text.rfind("]") + 1

#         if array_start != -1 and array_end != -1:
#             return json.loads(output_text[array_start:array_end])

#         obj_start = output_text.find("{")
#         obj_end = output_text.rfind("}") + 1

#         if obj_start != -1 and obj_end != -1:
#             return json.loads(output_text[obj_start:obj_end])

#         raise ValueError(f"No JSON found in LLM output:\n{output_text[:200]}")

#     except Exception as e:
#         raise CloudOptimizerException("LLM response invalid or API failed", e)


# if __name__ == "__main__":
#     prompt = """
# Return ONLY valid JSON.
# No explanation.

# {
#   "test": "success"
# }
# """
#     print(call_llm(prompt))




# For python test_profile_pipeline.py

# import os
# import json
# from dotenv import load_dotenv
# from mistralai.client import MistralClient

# from src.exception import CloudOptimizerException

# # Load environment variables from .env
# load_dotenv()

# # Read API key
# try:
#     MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
# except KeyError:
#     MISTRAL_API_KEY = None

# # Initialize the Mistral client
# client = MistralClient(api_key=MISTRAL_API_KEY)

# # Cost-effective model for free tier
# MODEL_NAME = "mistral-tiny"


# def call_llm(prompt: str) -> dict:
#     response = None
#     try:
#         # Construct messages for chat endpoint
#         messages = [
#             {"role": "user", "content": prompt}
#         ]

#         # Call streaming chat API
#         chat_response = client.chat_stream(
#             model=MODEL_NAME,
#             messages=messages,
#             temperature=0.0,
#             max_tokens=512,
#         )

#         # Collect streamed output
#         output_text = ""
#         for chunk in chat_response:
#             if chunk.choices and chunk.choices[0].delta.content is not None:
#                 output_text += chunk.choices[0].delta.content

#         # Extract JSON safely
#         start = output_text.find("{")
#         end = output_text.rfind("}") + 1

#         if start == -1 or end == -1:
#             print(f"DEBUG: Full LLM Output:\n{output_text}")
#             raise ValueError("No JSON found in LLM output")

#         return json.loads(output_text[start:end])

#     except Exception as e:
#         error_message = f"LLM response invalid or API failed: {e}"
#         raise CloudOptimizerException(error_message, e)


# if __name__ == "__main__":
#     prompt = """
# Return ONLY valid JSON.
# No explanation.

# {
#   "test": "success"
# }
# """
#     print(call_llm(prompt))
