from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from flask_login import login_required, current_user

from backend.extensions import db
from backend.models.resume_model import Resume
from backend.models.interview_model import Interview

from backend.services.aptitude_generator import (
    generate_aptitude_test
)

from backend.services.ai_interviewer import (
    generate_interview,
    evaluate_answer
)

from backend.services.code_evaluator import evaluate_submission
from backend.services.agent_memory import save_coding_result

interview = Blueprint(
    "interview",
    __name__
)


# ====================================
# SELECT ROLE
# ====================================
@interview.route(
    "/select_role",
    methods=["GET", "POST"]
)
@login_required
def select_role():

    if request.method == "POST":

        role = request.form.get("role")

        return redirect(
            url_for(
                "interview.interview_options",
                role=role
            )
        )

    return render_template(
        "select_role.html"
    )


# ====================================
# INTERVIEW OPTIONS
# ====================================
@interview.route(
    "/interview_options/<role>"
)
@login_required
def interview_options(role):

    return render_template(
        "interview_options.html",
        role=role
    )


# ====================================
# APTITUDE TEST
# ====================================
@interview.route(
    "/aptitude/<role>",
    methods=["GET", "POST"]
)
@login_required
def aptitude(role):

    if request.method == "GET":

        questions = generate_aptitude_test()

        session["aptitude_questions"] = questions

        return render_template(
            "aptitude.html",
            role=role,
            questions=questions
        )

    questions = session.get(
        "aptitude_questions",
        []
    )

    score = 0
    results = []

    for i, q in enumerate(
            questions,
            start=1):

        user_answer = request.form.get(
            f"q{i}"
        )

        if user_answer == q["answer"]:
            score += 1

        results.append({

            "question":
                q["question"],

            "user_answer":
                user_answer
                if user_answer
                else "Not Answered",

            "correct_answer":
                q["answer"]
        })

    total = len(questions)
    correct = score
    wrong = total - score

    percentage = 0

    if total > 0:
        percentage = round(
            (score / total) * 100,
            2
        )

    return render_template(
        "aptitude_result.html",
        role=role,
        score=score,
        total=total,
        correct=correct,
        wrong=wrong,
        percentage=percentage,
        results=results
    )


# ====================================
# TECHNICAL
# ====================================
from backend.services.technical_generator import (
    generate_technical_questions
)


@interview.route(
    "/technical/<role>",
    methods=["GET","POST"]
)
@login_required
def technical(role):

    if request.method == "GET":

        questions = generate_technical_questions(role)

        session["technical_questions"] = questions

        return render_template(
            "technical.html",
            role=role,
            questions=questions
        )

    questions = session.get(
        "technical_questions",
        []
    )

    score = 0
    results = []

    for i, q in enumerate(
        questions,
        start=1
    ):

        user_answer = request.form.get(
            f"q{i}"
        )

        if user_answer == q["answer"]:
            score += 1

        results.append({

            "question":
                q["question"],

            "user_answer":
                user_answer,

            "correct_answer":
                q["answer"]
        })

    total = len(questions)

    percentage = round(
        score / total * 100,
        2
    )

    return render_template(
        "technical_result.html",
        role=role,
        score=score,
        total=total,
        percentage=percentage,
        results=results
    )


# ====================================
# CODING
# ====================================
@interview.route(
    "/coding/<role>",
    methods=["GET", "POST"]
)
@login_required
def coding(role):

    languages = [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript"
    ]

    question = {
        "title": "Reverse a String",
        "description":
            "Write a program to reverse a string without using built-in reverse functions."
    }

    # OPEN CODING PAGE
    if request.method == "GET":

        return render_template(
            "coding.html",
            role=role,
            languages=languages,
            question=question
        )

    # ====================================
    # SUBMIT CODE
    # ====================================
    language = request.form.get(
        "language",
        ""
    )

    code = request.form.get(
        "code",
        ""
    )

    # Real AI code review (with automatic fallback to a basic
    # heuristic if the Gemini call fails)
    result = evaluate_submission(
        question["title"],
        question["description"],
        language,
        code
    )

    score = result["score"]
    grade = result["grade"]
    feedback = result["feedback"]

    # let the AI career agent know how this candidate does at coding
    save_coding_result(
        current_user.id,
        score
    )

    return render_template(
        "coding_result.html",
        role=role,
        language=language,
        code=code,
        score=score,
        grade=grade,
        suggestions=feedback
    )


# ====================================
# AI MOCK INTERVIEW
# ====================================
@interview.route(
    "/hr/<role>",
    methods=["GET", "POST"]
)
@login_required
def hr(role):

    # START INTERVIEW
    if request.method == "GET":

        # pull the candidate's latest resume so Gemini can
        # personalize the questions instead of using generic ones
        latest_resume = (
            Resume.query
            .filter_by(user_id=current_user.id)
            .order_by(Resume.id.desc())
            .first()
        )

        skills = []
        projects = []
        education = []

        if latest_resume:

            if latest_resume.skills:
                skills = [
                    s.strip()
                    for s in latest_resume.skills.split(",")
                    if s.strip()
                ]

            if latest_resume.projects:
                projects = [
                    p.strip()
                    for p in latest_resume.projects.split(",")
                    if p.strip()
                ]

            if latest_resume.education:
                education = [
                    e.strip()
                    for e in latest_resume.education.split(",")
                    if e.strip()
                ]

        questions = generate_interview(
            role=role,
            skills=skills,
            projects=projects,
            education=education
        )

        print("Questions:", questions)

        if not questions:

            return render_template(
                "error.html",
                message="No interview questions found."
            )

        session["interview_questions"] = questions
        session["current_question"] = 0
        session["interview_score"] = 0
        session["feedback"] = []

        first_question = questions[0]

        if isinstance(first_question, dict):
            first_question = first_question.get(
                "question",
                "Question not found"
            )

        return render_template(
            "hr_interview.html",
            role=role,
            question=first_question,
            current=1,
            total=len(questions)
        )

    # =================================
    # CONTINUE INTERVIEW
    # =================================

    questions = session.get(
        "interview_questions",
        []
    )

    current = session.get(
        "current_question",
        0
    )

    if current >= len(questions):

        return redirect(
            url_for(
                "interview.hr",
                role=role
            )
        )

    answer = request.form.get(
        "answer",
        ""
    )

    current_question = questions[current]

    if isinstance(current_question, dict):
        question_text = current_question.get(
            "question",
            ""
        )
    else:
        question_text = current_question

    score, feedback = evaluate_answer(
        question_text,
        answer
    )

    session["interview_score"] += score

    reviews = session.get(
        "feedback",
        []
    )

    reviews.append({

        "question":
            question_text,

        "answer":
            answer,

        "score":
            score,

        "feedback":
            feedback
    })

    session["feedback"] = reviews

    current += 1

    session["current_question"] = current

    # =================================
    # FINISH INTERVIEW
    # =================================
    if current >= len(questions):

        total_score = len(questions) * 100

        percentage = round(
            (
                session["interview_score"]
                / total_score
            ) * 100,
            2
        )

        if percentage >= 80:

            suggestion = (
                "Excellent performance. "
                "You are interview ready."
            )

        elif percentage >= 60:

            suggestion = (
                "Good performance. "
                "Improve communication "
                "and technical depth."
            )

        else:

            suggestion = (
                "Needs improvement. "
                "Practice aptitude, "
                "technical concepts "
                "and HR answers."
            )

        # =================================
        # SAVE THE INTERVIEW (this was
        # missing entirely before - nothing
        # was ever written to the database,
        # which is why "attended interviews"
        # never updated on the dashboard)
        # =================================
        interview_record = Interview(
            user_id=current_user.id,
            job_role=role,
            question="; ".join(
                r["question"] for r in reviews
            ),
            answer="; ".join(
                r["answer"] for r in reviews
            ),
            question_type="hr",
            overall_score=percentage,
            feedback=" || ".join(
                str(r["feedback"]) for r in reviews
            ),
            improvement=suggestion
        )

        db.session.add(interview_record)

        current_user.update_interview_stats(percentage)

        db.session.commit()

        final_score = session.get("interview_score", 0)

        # clear session state so the next attempt starts fresh
        session.pop("interview_questions", None)
        session.pop("current_question", None)
        session.pop("interview_score", None)
        session.pop("feedback", None)

        return render_template(
            "interview_report.html",
            role=role,
            score=final_score,
            percentage=percentage,
            results=reviews,
            suggestion=suggestion
        )

    # =================================
    # NEXT QUESTION
    # =================================
    next_question = questions[current]

    if isinstance(next_question, dict):
        next_question = next_question.get(
            "question",
            "Question not found"
        )

    return render_template(
        "hr_interview.html",
        role=role,
        question=next_question,
        current=current + 1,
        total=len(questions)
    )