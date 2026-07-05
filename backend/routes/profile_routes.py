from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from backend.extensions import db

# =====================================
# BLUEPRINT
# =====================================
profile = Blueprint(
    "profile",
    __name__
)


# =====================================
# PROFILE PAGE
# =====================================
@profile.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def user_profile():

    # =============================
    # UPDATE PROFILE
    # =============================
    if request.method == "POST":

        try:

            # -------------------------
            # PERSONAL DETAILS
            # -------------------------
            current_user.phone = request.form.get(
                "phone",
                ""
            )

            current_user.location = request.form.get(
                "location",
                ""
            )

            # -------------------------
            # EDUCATION
            # -------------------------
            current_user.college = request.form.get(
                "college",
                ""
            )

            current_user.degree = request.form.get(
                "degree",
                ""
            )

            current_user.specialization = request.form.get(
                "specialization",
                ""
            )

            current_user.graduation_year = request.form.get(
                "graduation_year",
                ""
            )

            # -------------------------
            # PROFESSIONAL LINKS
            # -------------------------
            current_user.linkedin = request.form.get(
                "linkedin",
                ""
            )

            current_user.github = request.form.get(
                "github",
                ""
            )

            current_user.portfolio = request.form.get(
                "portfolio",
                ""
            )

            # -------------------------
            # CAREER
            # -------------------------
            current_user.current_role = request.form.get(
                "current_role",
                ""
            )

            current_user.preferred_role = request.form.get(
                "preferred_role",
                ""
            )

            current_user.skills_summary = request.form.get(
                "skills_summary",
                ""
            )

            # -------------------------
            # ABOUT
            # -------------------------
            current_user.bio = request.form.get(
                "bio",
                ""
            )

            # -------------------------
            # SAVE CHANGES
            # -------------------------
            db.session.commit()

            flash(
                "Profile updated successfully!",
                "success"
            )

            return redirect(
                url_for(
                    "profile.user_profile"
                )
            )

        except Exception as e:

            db.session.rollback()

            print("PROFILE ERROR:", e)

            flash(
                f"Error updating profile: {str(e)}",
                "danger"
            )

            return redirect(
                url_for(
                    "profile.user_profile"
                )
            )

    # =============================
    # DISPLAY PROFILE
    # =============================
    return render_template(
        "profile.html",
        user=current_user
    )