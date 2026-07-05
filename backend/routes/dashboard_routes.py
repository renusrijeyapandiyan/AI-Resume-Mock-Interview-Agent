from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from backend.models.resume_model import Resume
from backend.models.interview_model import Interview

# AI Agent
try:
    from backend.services.agent_engine import run_agent
    from backend.services.agent_memory import save_user_state
except Exception as e:
    print("AI Agent import failed:", e)
    run_agent = None
    save_user_state = None


# ==========================================
# DASHBOARD BLUEPRINT
# ==========================================
dashboard = Blueprint(
    "dashboard",
    __name__
)


# ==========================================
# DASHBOARD HOME
# ==========================================
@dashboard.route("/dashboard")
@login_required
def dashboard_home():

    # =====================================
    # USER RESUMES
    # =====================================
    resumes = (
        Resume.query
        .filter_by(user_id=current_user.id)
        .order_by(Resume.id.desc())
        .all()
    )

    latest_resume = (
        resumes[0]
        if resumes
        else None
    )

    # =====================================
    # USER INTERVIEWS
    # =====================================
    interviews = (
        Interview.query
        .filter_by(user_id=current_user.id)
        .order_by(Interview.id.desc())
        .all()
    )

    total_interviews = len(interviews)

    # =====================================
    # ATS SCORE
    # =====================================
    ats_score = 0

    if latest_resume:
        ats_score = latest_resume.ats_score or 0

    # =====================================
    # INTERVIEW AVERAGE
    # =====================================
    scores = []

    for interview in interviews:
        if interview.overall_score is not None:
            scores.append(interview.overall_score)

    average_score = 0

    if len(scores) > 0:
        average_score = round(
            sum(scores) / len(scores),
            2
        )

    # =====================================
    # AI AGENT
    # =====================================
    # keep the agent's memory (AgentState) in sync with the real,
    # current DB records every time the dashboard loads - previously
    # this only happened on the /agent page, so if a user never
    # visited that page the dashboard's ATS score / interview count
    # would show stale (usually zero) numbers.
    if save_user_state:

        try:
            save_user_state(
                current_user.id,
                ats_score,
                average_score,
                total_interviews
            )
        except Exception as e:
            print("Failed to sync agent memory on dashboard:", e)

    if run_agent:

        try:
            agent = run_agent(
                current_user.id
            )

        except Exception as e:

            print("AI Agent execution failed on dashboard:", e)

            agent = {
                "status":
                    "Waiting",

                "message":
                    "Upload resume and attend interviews.",

                "action":
                    "Start your preparation.",

                "interview_count":
                    total_interviews
            }

    else:

        agent = {
            "status":
                "Waiting",

            "message":
                "AI Agent unavailable.",

            "action":
                "Configure AI Agent.",

            "interview_count":
                total_interviews
        }

    # =====================================
    # AGENT STATUS
    # =====================================
    agent_status = agent["status"]

    agent_recommendation = (
        agent["message"]
    )

    next_action = (
        agent["action"]
    )

    # =====================================
    # PROFILE STRENGTH
    # =====================================
    success_rate = int(
        (
            ats_score +
            average_score
        ) / 2
    )

    # =====================================
    # RENDER
    # =====================================
    return render_template(

        "dashboard.html",

        # database
        resumes=resumes,
        interviews=interviews,
        latest_resume=latest_resume,

        # statistics
        ats_score=ats_score,
        average_score=average_score,
        total_interviews=total_interviews,
        success_rate=success_rate,

        # agent
        agent=agent,
        agent_status=agent_status,
        agent_recommendation=agent_recommendation,
        next_action=next_action
    )