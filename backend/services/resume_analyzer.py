# backend/services/resume_analyzer.py

import re


# ====================================
# SKILL DATABASE
# ====================================
SKILLS_DB = [

    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "tensorflow",
    "pytorch",
    "mysql",
    "mongodb",
    "git",
    "aws",
    "data structures",
    "algorithms"
]


# ====================================
# EXTRACT SKILLS
# ====================================
def extract_skills(text):

    skills = []

    text = text.lower()

    for skill in SKILLS_DB:

        if skill.lower() in text:
            skills.append(skill)

    return list(set(skills))


# ====================================
# EXTRACT EMAIL
# ====================================
def extract_email(text):

    emails = re.findall(
        r'[\w\.-]+@[\w\.-]+',
        text
    )

    if emails:
        return emails[0]

    return ""


# ====================================
# EXTRACT PHONE
# ====================================
def extract_phone(text):

    phones = re.findall(
        r'\d{10}',
        text
    )

    if phones:
        return phones[0]

    return ""


# ====================================
# EXTRACT EDUCATION
# ====================================
def extract_education(text):

    education = []

    keywords = [

        "b.tech",
        "b.e",
        "m.tech",
        "mba",
        "bsc",
        "msc",
        "engineering",
        "college",
        "university"
    ]

    lines = text.split("\n")

    for line in lines:

        for keyword in keywords:

            if keyword in line.lower():

                education.append(
                    line.strip()
                )

                break

    return list(set(education))


# ====================================
# EXTRACT PROJECTS
# ====================================
def extract_projects(text):

    projects = []

    lines = text.split("\n")

    for line in lines:

        if (
            "project" in line.lower()
            or
            "developed" in line.lower()
            or
            "built" in line.lower()
        ):

            projects.append(
                line.strip()
            )

    return projects


# ====================================
# EXTRACT EXPERIENCE
# ====================================
def extract_experience(text):

    experience = []

    lines = text.split("\n")

    for line in lines:

        if (
            "intern" in line.lower()
            or
            "experience" in line.lower()
            or
            "worked" in line.lower()
        ):

            experience.append(
                line.strip()
            )

    return experience


# ====================================
# MAIN ANALYZER
# ====================================
def analyze_resume(text):

    return {

        "email":
            extract_email(text),

        "phone":
            extract_phone(text),

        "skills":
            extract_skills(text),

        "education":
            extract_education(text),

        "projects":
            extract_projects(text),

        "experience":
            extract_experience(text)
    }