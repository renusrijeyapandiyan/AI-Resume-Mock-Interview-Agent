from ai_engine.code_evaluator import (
    evaluate_code as gemini_evaluate_code
)


def _fallback_heuristic(code):
    """
    The original substring-based heuristic, kept only as a safety
    net if the Gemini call fails.
    """

    score = 0
    feedback = []

    if len(code) > 20:
        score += 40
    else:
        feedback.append("Write a more complete solution.")

    if "for" in code or "while" in code:
        score += 30
    else:
        feedback.append("Consider using loops.")

    if "print" in code or "return" in code:
        score += 30
    else:
        feedback.append("Your solution should return or print the result.")

    score = min(score, 100)

    if score >= 80:
        grade = "Excellent"
    elif score >= 60:
        grade = "Good"
    elif score >= 40:
        grade = "Average"
    else:
        grade = "Needs Improvement"

    if not feedback:
        feedback = [
            "Good solution.",
            "Try optimizing time complexity.",
            "Add comments for readability."
        ]

    return {
        "score": score,
        "grade": grade,
        "feedback": feedback
    }


def evaluate_submission(
        question_title,
        question_description,
        language,
        code):
    """
    Single entry point used by interview_routes.py's coding round.
    Tries Gemini first for real code review; falls back to the old
    substring heuristic if the AI call fails.
    """

    if not code or not code.strip():

        return {
            "score": 0,
            "grade": "Needs Improvement",
            "feedback": ["No code was submitted."]
        }

    try:

        result = gemini_evaluate_code(
            question_title,
            question_description,
            language,
            code
        )

        if result and "score" in result:

            return {
                "score": int(result.get("score", 0)),
                "grade": result.get("grade", "Average"),
                "feedback": result.get("feedback") or ["Evaluated."]
            }

    except Exception as e:

        print(
            "Gemini code evaluation failed, "
            "using fallback heuristic:",
            e
        )

    return _fallback_heuristic(code)
