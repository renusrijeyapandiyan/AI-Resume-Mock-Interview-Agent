def recommend_next_step(
        ats,
        aptitude,
        interview):

    if ats < 60:
        return (
            "Improve resume first"
        )

    if aptitude < 50:
        return (
            "Practice aptitude"
        )

    if interview < 60:
        return (
            "Practice HR interview"
        )

    return (
        "Proceed to coding round"
    )