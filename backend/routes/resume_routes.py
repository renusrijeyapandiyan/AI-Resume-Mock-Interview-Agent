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

from werkzeug.utils import secure_filename

from backend.extensions import db
from backend.models.resume_model import Resume
from backend.services.resume_parser import *
from backend.services.resume_ai_analyzer import analyze_resume_full

import os


# =====================================
# BLUEPRINT
# =====================================
resume = Blueprint(
    "resume",
    __name__
)


# =====================================
# UPLOAD RESUME
# =====================================
@resume.route(
    "/upload_resume",
    methods=["GET", "POST"]
)
@login_required
def upload_resume():

    if request.method == "POST":

        try:

            file = request.files.get("resume")

            # -----------------------------
            # Validate
            # -----------------------------
            if not file or file.filename == "":
                return render_template(
                    "upload_resume.html",
                    error="Please select a resume file."
                )

            filename = secure_filename(
                file.filename
            )

            # -----------------------------
            # Upload folder
            # -----------------------------
            upload_folder = (
                "backend/uploads/resumes"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            save_path = os.path.join(
                upload_folder,
                filename
            )

            file.save(save_path)

            # =====================================
            # RESUME ANALYSIS
            # =====================================
            resume_text = extract_resume_text(
                save_path
            )

            skills = extract_skills(
                resume_text
            )

            projects = extract_projects(
                resume_text
            )

            education = extract_education(
                resume_text
            )

            experience = extract_experience(
                resume_text
            )

            # =====================================
            # RESUME ANALYSIS (AI-powered, with
            # automatic fallback to rule-based scoring
            # if the Gemini call fails)
            # =====================================
            analysis = analyze_resume_full(
                resume_text,
                skills,
                projects,
                education,
                experience
            )

            ats_score = analysis["ats_score"]
            roles = analysis["recommended_roles"]

            # =====================================
            # CREATE RESUME OBJECT
            # =====================================
            resume_obj = Resume(

                user_id=current_user.id,

                file_name=filename,

                file_path=save_path,

                resume_text=resume_text,

                skills=", ".join(skills),

                projects=", ".join(projects),

                education=", ".join(education),

                experience=", ".join(experience),

                ats_score=ats_score,

                recommended_roles=", ".join(roles),

                missing_skills=", ".join(
                    analysis["missing_skills"]
                ),

                strengths=", ".join(
                    analysis["strengths"]
                ),

                weaknesses=", ".join(
                    analysis["weaknesses"]
                ),

                suggestions=", ".join(
                    analysis["suggestions"]
                )
            )

            # =====================================
            # UPDATE USER PROFILE
            # =====================================
            current_user.skills_summary = (
                ", ".join(skills)
            )

            if education:
                current_user.degree = education[0]

            if roles:
                current_user.preferred_role = roles[0]

            # update count correctly
            current_user.total_resumes = (
                Resume.query.filter_by(
                    user_id=current_user.id
                ).count() + 1
            )

            # =====================================
            # SAVE
            # =====================================
            db.session.add(
                resume_obj
            )

            db.session.commit()

            flash(
                "Resume uploaded successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "resume.resume_details",
                    resume_id=resume_obj.id
                )
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error: {str(e)}",
                "danger"
            )

            return redirect(
                url_for(
                    "resume.upload_resume"
                )
            )

    # =====================================
    # SHOW USER RESUMES
    # =====================================
    user_resumes = (
        Resume.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            Resume.id.desc()
        )
        .all()
    )

    return render_template(
        "upload_resume.html",
        resumes=user_resumes
    )


# =====================================
# RESUME DETAILS
# =====================================
@resume.route(
    "/resume/<int:resume_id>"
)
@login_required
def resume_details(resume_id):

    resume_data = (
        Resume.query
        .filter_by(
            id=resume_id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    return render_template(
        "resume_details.html",
        resume=resume_data
    )


# =====================================
# DELETE RESUME
# =====================================
@resume.route(
    "/delete_resume/<int:resume_id>"
)
@login_required
def delete_resume(resume_id):

    resume_data = (
        Resume.query
        .filter_by(
            id=resume_id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    try:

        # delete uploaded file
        if (
            resume_data.file_path and
            os.path.exists(
                resume_data.file_path
            )
        ):
            os.remove(
                resume_data.file_path
            )

        db.session.delete(
            resume_data
        )

        db.session.commit()

        # update count
        current_user.total_resumes = (
            Resume.query.filter_by(
                user_id=current_user.id
            ).count()
        )

        db.session.commit()

        flash(
            "Resume deleted successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            str(e),
            "danger"
        )

    return redirect(
        url_for(
            "resume.upload_resume"
        )
    )