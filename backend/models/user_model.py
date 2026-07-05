from backend.extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):

    __tablename__ = "users"

    # -------------------------
    # BASIC INFORMATION
    # -------------------------
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False, index=True)

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -------------------------
    # PROFILE INFORMATION
    # -------------------------
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))

    college = db.Column(db.String(150))
    degree = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    graduation_year = db.Column(db.String(20))

    linkedin = db.Column(db.String(255))
    github = db.Column(db.String(255))
    portfolio = db.Column(db.String(255))

    bio = db.Column(db.Text)
    profile_photo = db.Column(db.String(255))

    current_role = db.Column(db.String(100))
    preferred_role = db.Column(db.String(100))
    skills_summary = db.Column(db.Text)

    # -------------------------
    # GAMIFICATION
    # -------------------------
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    streak = db.Column(db.Integer, default=0)
    badge = db.Column(db.String(100), default="Beginner")

    # -------------------------
    # STATISTICS
    # -------------------------
    total_interviews = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0)
    total_resumes = db.Column(db.Integer, default=0)
    total_practice_hours = db.Column(db.Integer, default=0)

    # -------------------------
    # RELATIONSHIPS
    # -------------------------
    resumes = db.relationship(
        "Resume",
        backref="user",
        lazy=True,
        cascade="all, delete"
    )

    interviews = db.relationship(
        "Interview",
        backref="user",
        lazy=True,
        cascade="all, delete"
    )

    # -------------------------
    # AUTH METHODS (IMPORTANT FIX)
    # -------------------------
    def set_password(self, password):
        """Hash password before saving"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verify hashed password"""
        return check_password_hash(self.password, password)

    # -------------------------
    # GAMIFICATION METHODS
    # -------------------------
    def update_level(self):
        self.level = max(1, self.xp // 100 + 1)

        if self.level >= 20:
            self.badge = "Expert"
        elif self.level >= 10:
            self.badge = "Advanced"
        elif self.level >= 5:
            self.badge = "Intermediate"
        else:
            self.badge = "Beginner"

    def add_xp(self, points: int):
        self.xp += points
        self.update_level()

    # -------------------------
    # STATISTICS HELPERS
    # -------------------------
    def update_interview_stats(self, score: float):
        self.total_interviews += 1

        if self.total_interviews == 1:
            self.average_score = score
        else:
            self.average_score = (
                (self.average_score * (self.total_interviews - 1)) + score
            ) / self.total_interviews

    def add_practice_hours(self, hours: int):
        self.total_practice_hours += hours

    def increment_resume_count(self):
        self.total_resumes += 1

    # -------------------------
    # DEBUG / REPRESENTATION
    # -------------------------
    def __repr__(self):
        return f"<User {self.email}>"