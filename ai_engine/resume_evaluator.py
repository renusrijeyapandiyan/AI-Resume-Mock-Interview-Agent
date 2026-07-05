from ai_engine.gemini_api import generate_json


def evaluate_resume(
        resume_text,
        skills,
        projects,
        education,
        experience,
        target_role=None):
    """
    Uses Gemini to evaluate a resume the way a strict recruiter/ATS
    would - reading the actual content, not just counting keyword
    hits like the old regex-based scorer did.

    Returns a dict, or None if the AI call failed/was unusable
    (caller should fall back to the rule-based scorer in that case):

    {
      "ats_score": 0-100,
      "recommended_roles": [...],
      "missing_skills": [...],
      "strengths": [...],
      "weaknesses": [...],
      "suggestions": [...]
    }
    """

    # keep the prompt a reasonable size
    trimmed_text = resume_text[:6000] if resume_text else ""

    prompt = f"""
You are a strict, experienced technical recruiter and ATS (Applicant
Tracking System) reviewing a candidate's resume.

Raw resume text:
{trimmed_text}

Skills detected by our parser: {skills}
Projects detected by our parser: {projects}
Education detected by our parser: {education}
Experience detected by our parser: {experience}

Target role: {target_role or "not specified - infer the best fit from the resume"}

Score the resume out of 100 using this exact weighted rubric, then
report the final combined score as "ats_score":

1. Skill relevance & depth (0-30): Are the listed skills relevant,
   current, and does the resume show real depth (not just a list of
   buzzwords)?
2. Project quality & impact (0-25): Are projects specific, do they
   show real technical ownership, and do they mention outcomes or
   quantified results (e.g. "reduced load time by 40%")? Generic or
   vague projects score low here.
3. Experience relevance (0-20): Internships/work experience relevant
   to the target role, with concrete responsibilities.
4. Resume clarity & ATS-friendliness (0-15): Clear structure, no
   dense unreadable blocks of text, consistent formatting, no
   missing contact info.
5. Education & certifications (0-10): Relevant degree/coursework or
   certifications.

Don't reward keyword stuffing - a resume that lists 20 buzzwords with
no substantiation should score LOWER than one with 8 skills backed by
real, specific project evidence.

Return a JSON object shaped exactly like this:

{{
  "ats_score": 0-100,
  "rubric_breakdown": {{
    "skill_relevance": 0-30,
    "project_quality": 0-25,
    "experience_relevance": 0-20,
    "clarity_and_formatting": 0-15,
    "education": 0-10
  }},
  "recommended_roles": ["role 1", "role 2"],
  "missing_skills": ["skill they should learn or add"],
  "strengths": ["specific strength based on THIS resume"],
  "weaknesses": ["specific weakness based on THIS resume"],
  "suggestions": ["specific, actionable improvement"]
}}
"""

    return generate_json(prompt)
