from backend.extensions import db


class Profile(db.Model):

    __tablename__ = "profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True
    )

    full_name = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(150)
    )

    phone = db.Column(
        db.String(50)
    )

    location = db.Column(
        db.String(150)
    )

    linkedin = db.Column(
        db.String(255)
    )

    github = db.Column(
        db.String(255)
    )

    degree = db.Column(
        db.String(255)
    )

    college = db.Column(
        db.String(255)
    )

    cgpa = db.Column(
        db.String(20)
    )

    experience = db.Column(
        db.String(100)
    )

    preferred_role = db.Column(
        db.String(100)
    )

    objective = db.Column(
        db.Text
    )

    skills = db.Column(
        db.Text
    )

    profile_image = db.Column(
        db.String(255)
    )

    def __repr__(self):
        return f"<Profile {self.full_name}>"