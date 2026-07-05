def get_agent_recommendation(
        ats_score,
        interview_score):

    if ats_score < 60:
        return (
            "Improve your resume ATS score "
            "before attending interviews."
        )

    elif interview_score < 70:
        return (
            "Practice aptitude and "
            "technical interviews."
        )

    return (
        "You are ready to apply "
        "for jobs."
    )


def get_next_action(
        ats_score,
        interview_score,
        interviews):

    if ats_score < 60:
        return (
            "Upload an improved resume."
        )

    if interviews < 3:
        return (
            "Complete more mock interviews."
        )

    if interview_score < 70:
        return (
            "Take coding assessments."
        )

    return (
        "Start applying for jobs."
    )