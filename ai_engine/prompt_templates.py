def interview_prompt(
        resume,
        skills,
        projects,
        role):

    return f"""
You are an expert technical interviewer.

Candidate Target Role:
{role}

Candidate Skills:
{skills}

Candidate Projects:
{projects}

Candidate Resume:
{resume}

Generate:

1. Five technical questions.
2. Three behavioral questions.
3. Two project-based questions.

Rules:
- Questions must be specific to the candidate.
- Focus on the selected job role.
- Ask about projects and technologies used.
- Return only the questions.
"""