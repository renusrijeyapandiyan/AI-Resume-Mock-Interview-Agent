# backend/services/agent_memory.py
#
# Backed by the AgentState DB table so the agent's memory persists
# across server restarts (previously this was a plain Python dict
# that reset every restart).

from backend.extensions import db
from backend.models.agent_state_model import AgentState


def _get_or_create(user_id):

    state = AgentState.query.filter_by(
        user_id=user_id
    ).first()

    if not state:
        state = AgentState(user_id=user_id)
        db.session.add(state)

    return state


def save_user_state(
        user_id,
        ats_score,
        interview_score,
        interviews):

    state = _get_or_create(user_id)

    state.ats_score = ats_score
    state.interview_score = interview_score
    state.interviews = interviews

    db.session.commit()

    return state


def save_coding_result(user_id, score):
    """
    Records a coding-round score as a running average, so the agent
    knows how strong the candidate's coding ability is, not just
    their resume/interview stats.
    """

    state = _get_or_create(user_id)

    attempts = state.coding_attempts or 0

    if attempts == 0:
        state.coding_score = score
    else:
        state.coding_score = (
            (state.coding_score * attempts) + score
        ) / (attempts + 1)

    state.coding_attempts = attempts + 1

    db.session.commit()

    return state


def get_user_state(user_id):

    state = AgentState.query.filter_by(
        user_id=user_id
    ).first()

    if not state:

        return {
            "ats_score": 0,
            "interview_score": 0,
            "interviews": 0,
            "coding_score": 0,
            "coding_attempts": 0
        }

    return {
        "ats_score": state.ats_score,
        "interview_score": state.interview_score,
        "interviews": state.interviews,
        "coding_score": state.coding_score or 0,
        "coding_attempts": state.coding_attempts or 0
    }
