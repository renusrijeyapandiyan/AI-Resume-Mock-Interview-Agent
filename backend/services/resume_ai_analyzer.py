from backend.services import resume_parser as legacy

from ai_engine.resume_evaluator import (
    evaluate_resume as gemini_evaluate_resume
)


def analyze_resume_full(
        resume_text,
        skills,
        projects,
        education,
        experience,
        target_role=None):
    """
    Single entry point used by resume_routes.py. Tries Gemini first
    for real, content-aware ATS scoring and recommendations. Falls
    back to the original regex/rule-based logic in resume_parser.py
    if the AI call fails, so uploading a resume never breaks even if
    the API key is missing or the request errors out.

    Returns a dict:
    {
      "ats_score": int,
      "recommended_roles": [...],
      "missing_skills": [...],
      "strengths": [...],
      "weaknesses": [...],
      "suggestions": [...]
    }
    """

    try:

        result = gemini_evaluate_resume(
            resume_text,
            skills,
            projects,
            education,
            experience,
            target_role
        )

        if result and "ats_score" in result:

            print(
                "[Gemini] Resume evaluated live via Gemini API "
                f"- ats_score={result.get('ats_score')}"
            )

            ats_score = int(result.get("ats_score", 0))

            return {
                "ats_score": ats_score,

                "recommended_roles": (
                    result.get("recommended_roles")
                    or legacy.recommend_roles(skills)
                ),

                "missing_skills": (
                    result.get("missing_skills")
                    or legacy.find_missing_skills(skills)
                ),

                "strengths": (
                    result.get("strengths")
                    or legacy.find_strengths(skills, projects)
                ),

                "weaknesses": (
                    result.get("weaknesses")
                    or legacy.find_weaknesses(skills, experience)
                ),

                "suggestions": (
                    result.get("suggestions")
                    or legacy.generate_suggestions(ats_score)
                )
            }

    except Exception as e:

        print(
            "Gemini resume evaluation failed, "
            "using fallback rule-based scoring:",
            e
        )

    # ==========================================
    # FALLBACK: original rule-based logic
    # ==========================================
    ats_score = legacy.calculate_ats_score(
        skills,
        projects,
        education,
        experience,
        resume_text
    )

    return {
        "ats_score": ats_score,
        "recommended_roles": legacy.recommend_roles(skills),
        "missing_skills": legacy.find_missing_skills(skills),
        "strengths": legacy.find_strengths(skills, projects),
        "weaknesses": legacy.find_weaknesses(skills, experience),
        "suggestions": legacy.generate_suggestions(ats_score)
    }
