from backend.services.resume_agent import analyze_resume
from backend.services.interview_agent import analyze_interview
from backend.services.planner_agent import create_learning_plan
from backend.services.recommendation_agent import recommend_next_step


class AIMockInterviewAgent:

    def execute(
            self,
            user,
            resume,
            aptitude_score,
            interview_score):

        resume_result = analyze_resume(
            resume
        )

        interview_result = analyze_interview(
            interview_score
        )

        next_step = recommend_next_step(
            resume.ats_score,
            aptitude_score,
            interview_score
        )

        learning_plan = create_learning_plan({
            "skills":
            user.skills_summary
        })

        return {

            "resume_analysis":
                resume_result,

            "interview":
                interview_result,

            "next_action":
                next_step,

            "learning_plan":
                learning_plan
        }