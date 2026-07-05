def create_learning_plan(profile):

    plan = []

    if "Python" not in profile["skills"]:
        plan.append(
            "Learn Python"
        )

    plan.append(
        "Practice aptitude daily"
    )

    plan.append(
        "Attend mock interviews"
    )

    return plan