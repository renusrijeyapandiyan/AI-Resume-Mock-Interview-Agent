def analyze_resume(resume):

    recommendations = []

    if resume.ats_score < 70:
        recommendations.append(
            "Improve ATS score"
        )

    if "Python" not in resume.skills:
        recommendations.append(
            "Learn Python"
        )

    return recommendations