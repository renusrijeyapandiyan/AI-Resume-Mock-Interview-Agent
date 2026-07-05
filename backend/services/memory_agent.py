class MemoryAgent:

    @staticmethod
    def save_user_progress(session, key, value):
        session[key] = value

    @staticmethod
    def get_user_progress(session, key):
        return session.get(key)

    @staticmethod
    def get_profile(user):

        return {
            "role": user.preferred_role,
            "skills": user.skills_summary,
            "degree": user.degree,
            "experience": user.current_role
        }