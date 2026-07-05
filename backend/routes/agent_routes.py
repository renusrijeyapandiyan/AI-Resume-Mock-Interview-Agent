# backend/routes/agent_routes.py

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

from backend.services.agent_memory import (
    save_user_state
)

from backend.services.agent_engine import (
    run_agent
)

agent = Blueprint(
    "agent",
    __name__
)


@agent.route("/agent")
@login_required
def ai_agent():

    latest_resume = (
        Resume.query
        .filter_by(user_id=current_user.id)
        .order_by(Resume.id.desc())
        .first()
    )

    interviews = (
        Interview.query
        .filter_by(user_id=current_user.id)
        .all()
    )

    ats_score = 0

    if latest_resume:
        ats_score = latest_resume.ats_score

    interview_score = 0

    scores = [
        i.overall_score
        for i in interviews
        if i.overall_score
    ]

    if scores:
        interview_score = (
            sum(scores)
            / len(scores)
        )

    save_user_state(
        current_user.id,
        ats_score,
        interview_score,
        len(interviews)
    )

    recommendation = run_agent(
        current_user.id
    )

    return render_template(
        "agent.html",
        result=recommendation
    )