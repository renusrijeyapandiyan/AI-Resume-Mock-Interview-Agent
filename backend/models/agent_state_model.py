from backend.extensions import db
from datetime import datetime


class AgentState(db.Model):
    """
    Persists what the AI career agent knows about each user, so its
    memory survives server restarts (the old version kept this in a
    plain Python dict in memory, which wiped on every restart).
    """

    __tablename__ = "agent_states"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    ats_score = db.Column(
        db.Float,
        default=0
    )

    interview_score = db.Column(
        db.Float,
        default=0
    )

    interviews = db.Column(
        db.Integer,
        default=0
    )

    # running average of coding-round scores + how many attempted,
    # so the agent can factor coding ability into its recommendation
    coding_score = db.Column(
        db.Float,
        default=0
    )

    coding_attempts = db.Column(
        db.Integer,
        default=0
    )

    # last decision the agent made, so it can be shown on dashboards
    # or compared against next time without recomputing
    last_status = db.Column(
        db.String(100)
    )

    last_recommendation = db.Column(
        db.Text
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<AgentState user_id={self.user_id}>"
