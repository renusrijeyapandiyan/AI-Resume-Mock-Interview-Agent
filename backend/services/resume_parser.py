import re
import os
from pypdf import PdfReader
from docx import Document


# =====================================
# EXTRACT COMPLETE RESUME TEXT
# =====================================
def extract_resume_text(file_path):

    text = ""

    try:

        extension = os.path.splitext(file_path)[1].lower()

        # PDF FILE
        if extension == ".pdf":

            reader = PdfReader(file_path)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        # DOCX FILE
        elif extension == ".docx":

            doc = Document(file_path)

            for para in doc.paragraphs:
                text += para.text + "\n"

    except Exception as e:

        print("Resume extraction error:", e)

    return text


# =====================================
# EXTRACT NAME
# =====================================
def extract_name(text):

    lines = text.split("\n")

    for line in lines[:5]:

        line = line.strip()

        if (
            len(line.split()) >= 2
            and len(line) < 40
            and "@" not in line
        ):
            return line

    return ""


# =====================================
# EXTRACT EMAIL
# =====================================
def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group() if match else ""


# =====================================
# EXTRACT PHONE
# =====================================
def extract_phone(text):

    match = re.search(
        r"(\+91[\-\s]?)?[6-9]\d{9}",
        text
    )

    return match.group() if match else ""


# =====================================
# EXTRACT LINKEDIN
# =====================================
def extract_linkedin(text):

    match = re.search(
        r"https?://(?:www\.)?linkedin\.com/[^\s]+",
        text
    )

    return match.group() if match else ""


# =====================================
# EXTRACT GITHUB
# =====================================
def extract_github(text):

    match = re.search(
        r"https?://(?:www\.)?github\.com/[^\s]+",
        text
    )

    return match.group() if match else ""


# =====================================
# EXTRACT COLLEGE
# =====================================
def extract_college(text):

    keywords = [
        "college",
        "university",
        "engineering"
    ]

    for line in text.split("\n"):

        for key in keywords:

            if key in line.lower():
                return line

    return ""


# =====================================
# EXTRACT SKILLS
# =====================================
def extract_skills(text):

    skills_db = [
        "python",
        "java",
        "c",
        "c++",
        "html",
        "css",
        "javascript",
        "react",
        "nodejs",
        "mysql",
        "mongodb",
        "flask",
        "django",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "sql",
        "spring boot",
        "git",
        "github",
        "aws",
        "azure",
        "docker",
        "kubernetes",
        "power bi",
        "excel",
        "pandas",
        "numpy",
        "opencv",
        "nlp",
        "generative ai",
        "langchain",
        "llm"
    ]

    found = []

    lower = text.lower()

    for skill in skills_db:

        if skill in lower:
            found.append(skill)

    return list(set(found))


# =====================================
# EXTRACT PROJECTS
# =====================================
def extract_projects(text):

    projects = []

    for line in text.split("\n"):

        if any(
            word in line.lower()
            for word in [
                "project",
                "developed",
                "built",
                "implemented",
                "created"
            ]
        ):
            projects.append(line)

    return list(set(projects))


# =====================================
# EXTRACT EDUCATION
# =====================================
def extract_education(text):

    education = []

    keywords = [
        "b.tech",
        "b.e",
        "m.tech",
        "cgpa",
        "college",
        "university",
        "engineering"
    ]

    for line in text.split("\n"):

        for key in keywords:

            if key in line.lower():
                education.append(line)

    return list(set(education))


# =====================================
# EXTRACT EXPERIENCE
# =====================================
def extract_experience(text):

    experience = []

    keywords = [
        "internship",
        "experience",
        "developer",
        "engineer",
        "intern",
        "worked"
    ]

    for line in text.split("\n"):

        for key in keywords:

            if key in line.lower():
                experience.append(line)

    return list(set(experience))


# =====================================
# ATS SCORE
# =====================================
def calculate_ats_score(
        skills,
        projects,
        education,
        experience,
        text):

    score = 0

    score += min(len(skills) * 6, 40)
    score += min(len(projects) * 8, 25)
    score += min(len(education) * 5, 15)
    score += min(len(experience) * 8, 15)

    keywords = [
        "project",
        "developed",
        "built",
        "implemented",
        "system",
        "data"
    ]

    hits = sum(
        1
        for k in keywords
        if k in text.lower()
    )

    score += min(hits * 2, 10)

    return min(score, 100)


# =====================================
# RECOMMENDED ROLES
# =====================================
def recommend_roles(skills):

    skills = [s.lower() for s in skills]

    roles = []

    if "python" in skills:
        roles.append("Python Developer")

    if "java" in skills:
        roles.append("Java Developer")

    if (
        "machine learning" in skills
        or "tensorflow" in skills
        or "pytorch" in skills
    ):
        roles.append("AI/ML Engineer")

    if (
        "html" in skills
        and "css" in skills
        and "javascript" in skills
    ):
        roles.append("Frontend Developer")

    if (
        "react" in skills
        or "nodejs" in skills
    ):
        roles.append("Full Stack Developer")

    if (
        "sql" in skills
        or "power bi" in skills
    ):
        roles.append("Data Analyst")

    if not roles:
        roles.append("Software Developer")

    return roles


# =====================================
# MISSING SKILLS
# =====================================
def find_missing_skills(skills):

    market = [
        "git",
        "github",
        "sql",
        "aws",
        "docker",
        "react"
    ]

    return [
        s
        for s in market
        if s not in skills
    ]


# =====================================
# STRENGTHS
# =====================================
def find_strengths(skills, projects):

    strengths = []

    if len(skills) >= 5:
        strengths.append(
            "Strong technical skills"
        )

    if len(projects) >= 2:
        strengths.append(
            "Good project experience"
        )

    return strengths


# =====================================
# WEAKNESSES
# =====================================
def find_weaknesses(
        skills,
        experience):

    weaknesses = []

    if len(experience) == 0:
        weaknesses.append(
            "No experience/internship section"
        )

    if len(skills) < 5:
        weaknesses.append(
            "Low skill coverage"
        )

    return weaknesses


# =====================================
# SUGGESTIONS
# =====================================
def generate_suggestions(score):

    suggestions = []

    if score < 70:

        suggestions.extend([
            "Add more projects",
            "Add certifications",
            "Improve technical skills",
            "Include quantified achievements"
        ])

    return suggestions