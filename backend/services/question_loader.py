import json
import os
import random

BASE = "backend/data"


def load_json(file):

    with open(
        os.path.join(BASE,file),
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def get_hr_questions(count=5):

    data = load_json(
        "hr_questions.json"
    )

    return random.sample(
        data["questions"],
        min(count,
            len(data["questions"]))
    )


def get_aptitude_questions(count=5):

    data = load_json(
        "aptitude_questions.json"
    )

    return random.sample(
        data["questions"],
        min(count,
            len(data["questions"]))
    )


def get_technical_questions(
        role,
        count=5):

    data = load_json(
        "technical_questions.json"
    )

    role = role.lower()

    if role in data:

        return random.sample(
            data[role],
            min(count,
                len(data[role]))
        )

    return []


def get_coding_questions(
        language,
        count=5):

    data = load_json(
        "coding_questions.json"
    )

    language = language.lower()

    if language in data:

        return random.sample(
            data[language],
            min(count,
                len(data[language]))
        )

    return []