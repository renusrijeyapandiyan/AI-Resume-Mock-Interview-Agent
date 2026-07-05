from ai_engine.gemini_api import generate_json


FALLBACK_RESULT = {
    "technical_score": 5,
    "communication_score": 5,
    "problem_solving_score": 5,
    "strengths": ["Basic understanding shown"],
    "weaknesses": ["Needs more depth"],
    "suggestions": ["Practice more with concrete examples"],
    "overall_feedback": "Average performance."
}


def evaluate_answer(
        question,
        answer):
    """
    Uses Gemini to evaluate a candidate's interview answer
    semantically (not just keyword matching).

    Returns a dict:
    {
        "technical_score": 0-10,
        "communication_score": 0-10,
        "problem_solving_score": 0-10,
        "strengths": [...],
        "weaknesses": [...],
        "suggestions": [...],
        "overall_feedback": "..."
    }

    Falls back to a safe default dict if the API call fails.
    """

    if not answer or not answer.strip():

        return {
            "technical_score": 0,
            "communication_score": 0,
            "problem_solving_score": 0,
            "strengths": [],
            "weaknesses": ["No answer was provided"],
            "suggestions": ["Attempt every question, even partially"],
            "overall_feedback": "No answer provided."
        }

    prompt = f"""
You are an expert technical interviewer evaluating a candidate's
spoken/written interview answer.

Question:
{question}

Candidate Answer:
{answer}

Score the answer honestly on a scale of 0-10 for each category.
Be specific and reference the actual content of the answer in your
feedback, don't give generic advice.

Return a JSON object shaped exactly like:
{{
  "technical_score": 0-10,
  "communication_score": 0-10,
  "problem_solving_score": 0-10,
  "strengths": ["short point", "short point"],
  "weaknesses": ["short point", "short point"],
  "suggestions": ["short actionable point"],
  "overall_feedback": "1-2 sentence summary"
}}
"""

    try:

        result = generate_json(prompt)

        if result and isinstance(result, dict) and "technical_score" in result:
            return result

    except Exception as e:

        print(
            "Gemini evaluation failed:",
            e
        )

    return FALLBACK_RESULT
