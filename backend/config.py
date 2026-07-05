import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # ------------------------
    # SECURITY
    # ------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    # ------------------------
    # DATABASE
    # ------------------------
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///database.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ------------------------
    # UPLOAD SETTINGS
    # ------------------------
    UPLOAD_FOLDER = os.path.join("backend", "uploads", "resumes")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

    # ------------------------
    # SESSION SETTINGS (IMPORTANT FOR LOGIN STABILITY)
    # ------------------------
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # set True in production (HTTPS)

    # ------------------------
    # OPTIONAL: DEBUG CONTROL
    # ------------------------
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"