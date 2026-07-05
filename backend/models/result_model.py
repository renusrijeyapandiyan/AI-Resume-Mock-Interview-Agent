from backend.extensions import db


class Result(db.Model):

    __tablename__ = "results"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    interview_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "interviews.id"
        )
    )

    technical_score = db.Column(
        db.Integer
    )

    communication_score = db.Column(
        db.Integer
    )

    problem_solving_score = db.Column(
        db.Integer
    )

    overall_score = db.Column(
        db.Integer
    )

    feedback = db.Column(
        db.Text
    )