import json
import random
import os


QUESTION_FILE = os.path.join(
    "backend",
    "data",
    "interview_questions.json"
)


# ====================================
# LOAD QUESTION DATABASE
# ====================================
def load_questions():

    try:

        with open(
            QUESTION_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception as e:

        print(
            "Question database error:",
            e
        )

        return {}


# ====================================
# GENERATE INTERVIEW QUESTIONS
# ====================================
def generate_questions(
        skills=None,
        count=15):

    if skills is None:
        skills = []

    database = load_questions()

    selected = []

    # ==========================
    # HR QUESTIONS
    # ==========================
    hr_questions = database.get(
        "hr",
        []
    )

    if hr_questions:

        selected.extend(

            random.sample(
                hr_questions,
                min(
                    5,
                    len(hr_questions)
                )
            )
        )

    # ==========================
    # APTITUDE QUESTIONS
    # ==========================
    aptitude_questions = database.get(
        "aptitude",
        []
    )

    if aptitude_questions:

        selected.extend(

            random.sample(
                aptitude_questions,
                min(
                    3,
                    len(aptitude_questions)
                )
            )
        )

    # ==========================
    # TECHNICAL QUESTIONS
    # ==========================
    for skill in skills:

        skill = skill.lower()

        questions = database.get(
            skill,
            []
        )

        if questions:

            selected.extend(

                random.sample(
                    questions,
                    min(
                        3,
                        len(questions)
                    )
                )
            )

    # ==========================
    # DEFAULT QUESTIONS
    # ==========================
    if len(selected) == 0:

        selected = [

            {
                "question":
                "Tell me about yourself."
            },

            {
                "question":
                "Explain your final year project."
            },

            {
                "question":
                "What are your strengths?"
            },

            {
                "question":
                "Why should we hire you?"
            },

            {
                "question":
                "Describe a challenging situation."
            }
        ]

    # ==========================
    # REMOVE DUPLICATES
    # ==========================
    unique = []

    seen = set()

    for q in selected:

        question = q.get(
            "question",
            ""
        )

        if question not in seen:

            seen.add(
                question
            )

            unique.append(
                q
            )

    random.shuffle(
        unique
    )

    return unique[:count]


# ====================================
# BACKWARD COMPATIBILITY
# ====================================
def generate_interview_questions(
        skills=None,
        count=15):

    return generate_questions(
        skills,
        count
    )