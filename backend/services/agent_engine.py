# backend/services/agent_engine.py

from backend.extensions import db
from backend.models.agent_state_model import AgentState

from backend.services.agent_memory import (
    get_user_state
)

from ai_engine.gemini_api import generate_json


# =====================================
# RULE-BASED SAFETY NET
# =====================================
# Used only if the Gemini call fails (no API key, network error,
# bad response, etc.) so the feature never breaks for the user.
def _rule_based_decision(ats, interview, coding, count):

    if ats < 60:

        return {
            "status": "Resume Improvement",
            "message": (
                "Your resume ATS score is low. "
                "Improve skills, projects, and certifications."
            ),
            "action": "Upload an improved resume.",
            "recommendation": "Focus on resume optimization."
        }

    elif interview < 70:

        return {
            "status": "Interview Training",
            "message": "Your interview performance needs improvement.",
            "action": "Practice technical interviews.",
            "recommendation": "Complete mock interviews."
        }

    elif coding < 60:

        return {
            "status": "Coding Practice",
            "message": "Your coding round performance needs work.",
            "action": "Attempt more coding problems.",
            "recommendation": "Practice data structures and algorithms daily."
        }

    elif count < 5:

        return {
            "status": "Practice Mode",
            "message": "You need more interview practice.",
            "action": "Take additional interviews.",
            "recommendation": "Complete at least 5 mock interviews."
        }

    return {
        "status": "Placement Ready",
        "message": "You are ready for placements.",
        "action": "Start applying for jobs.",
        "recommendation": "Apply for software and AI roles."
    }


# =====================================
# MAIN AI CAREER AGENT
# =====================================
def run_agent(user_id):
    """
    This is the real agent brain. Instead of hardcoded if/else
    thresholds, it hands the candidate's current stats - resume ATS
    score, mock interview average, AND coding round performance - to
    Gemini and asks it to reason about what they should do next, the
    same way a human career coach would look at all three signals
    together.

    If the AI call fails for any reason, it falls back to the old
    rule-based logic so the feature degrades gracefully instead of
    crashing.
    """

    state = get_user_state(user_id)

    ats = state.get("ats_score", 0)
    interview = state.get("interview_score", 0)
    coding = state.get("coding_score", 0)
    coding_attempts = state.get("coding_attempts", 0)
    count = state.get("interviews", 0)

    prompt = f"""
You are an AI career coaching agent inside a resume + mock interview
prep platform. You are looking at one candidate's current stats and
deciding the single most useful next step for them.

Candidate data:
- Resume ATS score: {ats}/100
- Average mock interview score: {interview}/100
- Number of mock interviews completed so far: {count}
- Average coding round score: {coding}/100
- Coding problems attempted so far: {coding_attempts}

Reason about where this candidate is weakest across ALL THREE areas
(resume, interviewing, coding) and decide what would help them most
right now. Don't just default to the first weak number - weigh all
three together as a human career coach would.

Respond with a JSON object shaped exactly like this:

{{
  "status": "a short 2-4 word status label, e.g. Resume Improvement",
  "message": "1-2 sentences explaining where they currently stand and why",
  "action": "one specific, concrete next action for them to take right now",
  "recommendation": "one sentence of practical advice or encouragement"
}}
"""

    result = generate_json(prompt)

    if result and all(
        key in result
        for key in ("status", "message", "action", "recommendation")
    ):
        print(
            "[Gemini] Agent decision made live via Gemini API "
            f"- status={result.get('status')}"
        )

    if not result or not all(
        key in result
        for key in ("status", "message", "action", "recommendation")
    ):

        print(
            "Agent reasoning via Gemini failed or returned an "
            "incomplete response - using rule-based fallback."
        )

        result = _rule_based_decision(ats, interview, coding, count)

    # =================================
    # EXTRA DASHBOARD DATA
    # =================================
    profile_strength = int(
        (ats * 0.5) + (interview * 0.3) + (coding * 0.2)
    )

    result["ats_score"] = ats
    result["interview_average"] = interview
    result["interview_count"] = count
    result["coding_score"] = coding
    result["coding_attempts"] = coding_attempts
    result["profile_strength"] = profile_strength
    result["placement_readiness"] = profile_strength

    # =================================
    # PERSIST THE AGENT'S DECISION
    # =================================
    # so the agent "remembers" its last verdict for this user
    state_row = AgentState.query.filter_by(user_id=user_id).first()

    if state_row:

        state_row.last_status = result.get("status")
        state_row.last_recommendation = result.get("recommendation")

        db.session.commit()

    return result
