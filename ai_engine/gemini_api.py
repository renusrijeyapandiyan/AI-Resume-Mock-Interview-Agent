import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception(
        "GEMINI_API_KEY not found in .env file"
    )

# Configure Gemini
genai.configure(
    api_key=API_KEY
)

# Model name is now configurable via .env (GEMINI_MODEL).
# If Google deprecates a model string, just change it in .env -
# no code change needed.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Create model
model = genai.GenerativeModel(
    model_name=MODEL_NAME
)


def generate_response(prompt):
    """
    Generic Gemini response function.
    Returns plain text, or None if the call failed.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print(
            "Gemini Error:",
            str(e)
        )

        return None


def generate_json(prompt, retries=1):
    """
    Asks Gemini to return JSON and parses it safely.
    Returns a Python dict/list, or None if it could not
    get valid JSON back (caller should fall back to
    rule-based logic in that case).
    """

    full_prompt = (
        prompt
        + "\n\nRespond with ONLY valid JSON. "
          "No markdown formatting, no ```json fences, "
          "no explanation text before or after."
    )

    attempt = 0

    while attempt <= retries:

        raw = generate_response(full_prompt)

        if not raw:
            attempt += 1
            continue

        cleaned = raw.strip()

        # Strip markdown code fences if Gemini adds them anyway
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except Exception as e:
            print("Gemini JSON parse error:", e, "| raw:", raw[:200])
            attempt += 1

    return None


def test_connection():
    """
    Test Gemini API
    """

    try:

        response = model.generate_content(
            "Say Hello"
        )

        print(
            "Gemini Connected Successfully"
        )

        print(
            response.text
        )

        return True

    except Exception as e:

        print(
            "Gemini Connection Failed"
        )

        print(e)

        return False


if __name__ == "__main__":
    test_connection()
