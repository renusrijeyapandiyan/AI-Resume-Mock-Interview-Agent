from backend.extensions import db
from datetime import datetime


class Resume(db.Model):

    __tablename__ = "resumes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # uploaded resume
    file_name = db.Column(
        db.String(255)
    )

    file_path = db.Column(
        db.String(500)
    )

    # complete extracted resume
    resume_text = db.Column(
        db.Text
    )

    # extracted sections
    skills = db.Column(
        db.Text
    )

    projects = db.Column(
        db.Text
    )

    education = db.Column(
        db.Text
    )

    experience = db.Column(
        db.Text
    )

    # scores
    ats_score = db.Column(
        db.Integer,
        default=0
    )

    job_match_score = db.Column(
        db.Integer,
        default=0
    )

    # recommendations
    recommended_roles = db.Column(
        db.Text
    )

    missing_skills = db.Column(
        db.Text
    )

    strengths = db.Column(
        db.Text
    )

    weaknesses = db.Column(
        db.Text
    )

    suggestions = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Resume {self.file_name}>"