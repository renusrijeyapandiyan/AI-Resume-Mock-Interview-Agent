from ai_engine.gemini_api import generate_json


def evaluate_code(
        question_title,
        question_description,
        language,
        code):
    """
    Uses Gemini to actually read and judge a coding submission -
    correctness, logic, and quality - instead of just checking
    whether certain substrings like "for" or "print" appear in the
    code (which the old version did).

    Returns a dict, or None if the AI call failed (caller should
    fall back to the old heuristic in that case):

    {
      "score": 0-100,
      "grade": "Excellent" | "Good" | "Average" | "Needs Improvement",
      "correct": true/false,
      "feedback": ["specific point", ...]
    }
    """

    prompt = f"""
You are a strict but fair technical interviewer reviewing a coding
round submission.

Problem: {question_title}
Description: {question_description}
Language the candidate used: {language}

Candidate's code:
{code}

Actually read this code. Judge whether it is logically correct,
whether it would run without errors in {language}, and how good the
approach/efficiency is. If it's broken, incomplete, or wouldn't
compile, say so plainly instead of being generically encouraging.

Return a JSON object shaped exactly like this:

{{
  "score": 0-100,
  "grade": "Excellent" or "Good" or "Average" or "Needs Improvement",
  "correct": true or false,
  "feedback": ["specific point about THIS code", "another specific point"]
}}
"""

    return generate_json(prompt)
