from ai_engine.gemini_api import generate_json


DEFAULT_QUESTIONS = [
    {"question": "Tell me about yourself.", "type": "hr"},
    {"question": "Explain your final year project.", "type": "project"},
    {"question": "What are your strengths?", "type": "hr"},
    {"question": "Explain OOP concepts.", "type": "technical"},
    {"question": "What is machine learning?", "type": "technical"},
    {"question": "Difference between SQL and NoSQL?", "type": "technical"},
    {"question": "Explain your internship.", "type": "experience"},
    {"question": "Describe a challenging problem you solved.", "type": "problem_solving"},
    {"question": "Why should we hire you?", "type": "hr"},
    {"question": "Where do you see yourself in 5 years?", "type": "hr"},
]


def generate_questions(
        skills,
        projects,
        education,
        job_role):
    """
    Uses Gemini to generate interview questions tailored to the
    candidate's actual resume data. Falls back to a sensible
    default set if the API call fails or returns something
    unusable, so the interview flow never breaks.

    Returns: list of dicts -> [{"question": str, "type": str}, ...]
    """

    prompt = f"""
You are an expert technical interviewer preparing a mock interview.

Candidate Skills:
{skills}

Candidate Projects:
{projects}

Candidate Education:
{education}

Target Job Role:
{job_role}

Generate exactly 10 interview questions tailored to this specific
candidate (reference their actual skills/projects where relevant,
don't just ask generic questions).

Include a mix of:
1. Resume/background questions
2. Project deep-dive questions
3. Technical questions matching their listed skills
4. Problem-solving questions
5. HR/behavioral questions

Return a JSON array of exactly 10 objects, each shaped like:
{{"question": "the question text", "type": "hr|technical|project|problem_solving|experience"}}
"""

    try:

        questions = generate_json(prompt)

        if questions and isinstance(questions, list) and len(questions) > 0:

            cleaned = []

            for q in questions:

                if isinstance(q, dict) and q.get("question"):

                    cleaned.append({
                        "question": q.get("question"),
                        "type": q.get("type", "general")
                    })

                elif isinstance(q, str):

                    cleaned.append({
                        "question": q,
                        "type": "general"
                    })

            if cleaned:
                return cleaned

    except Exception as e:

        print(
            "Gemini question generation failed:",
            e
        )

    return DEFAULT_QUESTIONS
