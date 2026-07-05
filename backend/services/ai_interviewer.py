import random

from backend.services.resume_analyzer import (
    analyze_resume
)

from backend.services.question_generator import (
    generate_interview_questions
)

from backend.services.interview_scorer import (
    score_answer
)

# Real Gemini-backed generation/evaluation
from ai_engine.interview_generator import (
    generate_questions as gemini_generate_questions
)

from ai_engine.evaluator import (
    evaluate_answer as gemini_evaluate_answer
)


# ==========================================
# FUNCTIONS USED BY interview_routes.py
# ==========================================
def generate_interview(
        role=None,
        skills=None,
        projects=None,
        education=None):
    """
    Generates interview questions using Gemini, personalized to the
    candidate's resume data when available. Falls back to the static
    question bank (question_generator.py) if the AI call fails, so
    the interview flow always works even if the API key is missing
    or the request errors out.
    """

    role = role or "Software Engineer"

    skills = skills or [
        "python",
        "java",
        "sql",
        "machine learning"
    ]

    projects = projects or []
    education = education or []

    try:

        questions = gemini_generate_questions(
            skills,
            projects,
            education,
            role
        )

        if questions:
            return questions

    except Exception as e:

        print(
            "Gemini interview generation failed, "
            "using fallback question bank:",
            e
        )

    return generate_interview_questions(
        skills=skills,
        count=10
    )


def evaluate_answer(
        question,
        answer):
    """
    Evaluates a candidate's answer using Gemini for semantic scoring
    (not just keyword matching). Falls back to the old keyword-based
    scorer if the AI call fails.

    Keeps the original (score, feedback) return contract so
    interview_routes.py does not need to change.
    """

    try:

        result = gemini_evaluate_answer(
            question,
            answer
        )

        if result and "technical_score" in result:

            technical = result.get("technical_score", 0)
            communication = result.get("communication_score", 0)
            problem_solving = result.get("problem_solving_score", 0)

            # each field is 0-10 -> average, scale to 0-100
            overall_score = round(
                ((technical + communication + problem_solving) / 3) * 10
            )

            feedback_parts = []

            if result.get("overall_feedback"):
                feedback_parts.append(result["overall_feedback"])

            if result.get("strengths"):
                feedback_parts.append(
                    "Strengths: " + "; ".join(result["strengths"])
                )

            if result.get("weaknesses"):
                feedback_parts.append(
                    "To improve: " + "; ".join(result["weaknesses"])
                )

            feedback = " | ".join(feedback_parts) if feedback_parts else "Evaluated."

            return overall_score, feedback

    except Exception as e:

        print(
            "Gemini answer evaluation failed, "
            "using fallback scorer:",
            e
        )

    result = score_answer(
        question,
        answer,
        []
    )

    return (
        result["score"],
        result["feedback"]
    )


# ==========================================
# AI INTERVIEWER CLASS
# ==========================================
class AIInterviewer:

    # ==========================
    # INITIALIZE INTERVIEW
    # ==========================
    def __init__(
            self,
            resume_text):

        self.resume_data = analyze_resume(
            resume_text
        )

        skills = self.resume_data.get(
            "skills",
            []
        )

        self.questions = generate_interview_questions(
            skills=skills,
            count=15
        )

        self.current_question = 0
        self.answers = []
        self.scores = []

    # ==========================
    # GET QUESTION
    # ==========================
    def get_question(self):

        if self.current_question >= len(
                self.questions):
            return None

        return self.questions[
            self.current_question
        ]

    # ==========================
    # SUBMIT ANSWER
    # ==========================
    def submit_answer(
            self,
            answer):

        if self.current_question >= len(
                self.questions):
            return None

        question = self.questions[
            self.current_question
        ]

        keywords = self.resume_data.get(
            "skills",
            []
        )

        result = score_answer(
            question,
            answer,
            keywords
        )

        self.answers.append({

            "question":
                question,

            "answer":
                answer,

            "score":
                result.get(
                    "score",
                    0
                ),

            "feedback":
                result.get(
                    "feedback",
                    ""
                )
        })

        self.scores.append(
            result.get(
                "score",
                0
            )
        )

        self.current_question += 1

        return result

    # ==========================
    # CHECK FINISHED
    # ==========================
    def is_finished(self):

        return (
            self.current_question
            >=
            len(self.questions)
        )

    # ==========================
    # GENERATE REPORT
    # ==========================
    def generate_report(self):

        if len(self.scores) == 0:

            return {

                "score": 0,
                "grade": "No Data",
                "total_questions": 0,
                "answers": [],
                "suggestions": []
            }

        average = (
            sum(self.scores)
            /
            len(self.scores)
        )

        if average >= 80:
            grade = "Excellent"

        elif average >= 60:
            grade = "Good"

        elif average >= 40:
            grade = "Average"

        else:
            grade = "Needs Improvement"

        suggestions = []

        if average < 60:

            suggestions.extend([

                "Improve technical concepts.",

                "Practice aptitude questions.",

                "Provide more detailed answers.",

                "Improve communication skills."
            ])

        else:

            suggestions.extend([

                "Improve confidence.",

                "Use real-world examples.",

                "Maintain consistency."
            ])

        return {

            "score":
                round(
                    average,
                    2
                ),

            "grade":
                grade,

            "total_questions":
                len(
                    self.answers
                ),

            "answers":
                self.answers,

            "suggestions":
                suggestions
        }