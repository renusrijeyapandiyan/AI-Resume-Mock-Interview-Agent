from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from backend.extensions import db, bcrypt
from backend.models.user_model import User


# ==========================================
# AUTH BLUEPRINT
# ==========================================
auth = Blueprint(
    "auth",
    __name__
)


# ==========================================
# REGISTER
# ==========================================
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing = User.query.filter_by(
            email=email
        ).first()

        if existing:
            flash("Email already exists")
            return redirect(
                url_for("auth.register")
            )

        hashed_password = (
            bcrypt.generate_password_hash(password)
            .decode("utf-8")
        )

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful")

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


# ==========================================
# LOGIN
# ==========================================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if (
            user and
            bcrypt.check_password_hash(
                user.password,
                password
            )
        ):

            login_user(user)

            return redirect(
                url_for(
                    "dashboard.dashboard_home"
                )
            )

        flash("Invalid credentials")

    return render_template(
        "login.html"
    )


# ==========================================
# LOGOUT
# ==========================================
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for(
            "auth.login"
        )
    )