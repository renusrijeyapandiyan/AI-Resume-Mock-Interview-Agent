from backend.extensions import db
from datetime import datetime


class Interview(db.Model):

    __tablename__ = "interviews"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    job_role = db.Column(
        db.String(100)
    )

    experience_level = db.Column(
        db.String(50)
    )

    difficulty = db.Column(
        db.String(50),
        default="Easy"
    )

    question = db.Column(
        db.Text
    )

    answer = db.Column(
        db.Text
    )

    question_type = db.Column(
        db.String(50)
    )

    technical_score = db.Column(
        db.Integer,
        default=0
    )

    communication_score = db.Column(
        db.Integer,
        default=0
    )

    confidence_score = db.Column(
        db.Integer,
        default=0
    )

    problem_solving_score = db.Column(
        db.Integer,
        default=0
    )

    overall_score = db.Column(
        db.Float,
        default=0
    )

    feedback = db.Column(
        db.Text
    )

    improvement = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Interview {self.job_role}>"