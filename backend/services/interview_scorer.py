

# backend/services/interview_scorer.py

def score_answer(
        question,
        answer,
        keywords=None):

    if keywords is None:
        keywords = []

    answer = answer.lower()

    score = 0
    matched = []

    # ======================
    # KEYWORD MATCHING
    # ======================
    for keyword in keywords:

        if keyword.lower() in answer:
            score += 15
            matched.append(keyword)

    # ======================
    # ANSWER LENGTH
    # ======================
    word_count = len(answer.split())

    if word_count >= 80:
        score += 40

    elif word_count >= 50:
        score += 30

    elif word_count >= 20:
        score += 20

    elif word_count >= 10:
        score += 10

    # ======================
    # CONFIDENCE WORDS
    # ======================
    confidence_words = [

        "implemented",
        "developed",
        "designed",
        "created",
        "optimized",
        "improved",
        "managed",
        "achieved",
        "built",
        "deployed",
        "solved",
        "worked",
        "experience",
        "project"
    ]

    confidence_score = 0

    for word in confidence_words:

        if word in answer:
            confidence_score += 5

    score += confidence_score

    # ======================
    # NORMALIZE
    # ======================
    if score > 100:
        score = 100

    # ======================
    # FEEDBACK
    # ======================
    strengths = []
    improvements = []

    if len(matched) > 0:
        strengths.append(
            "Used relevant technical keywords"
        )
    else:
        improvements.append(
            "Include more technical concepts"
        )

    if word_count >= 50:
        strengths.append(
            "Provided detailed explanation"
        )
    else:
        improvements.append(
            "Give more detailed answers"
        )

    if confidence_score > 0:
        strengths.append(
            "Demonstrated practical experience"
        )
    else:
        improvements.append(
            "Add project examples and experiences"
        )

    # ======================
    # FINAL FEEDBACK
    # ======================
    if score >= 80:
        feedback = "Excellent answer"

    elif score >= 60:
        feedback = "Good answer"

    elif score >= 40:
        feedback = "Average answer"

    else:
        feedback = "Needs improvement"

    return {

        "score": score,

        "feedback": feedback,

        "matched_keywords": matched,

        "strengths": strengths,

        "improvements": improvements
    }