def analyze_aptitude(score):

    if score >= 8:
        return "Ready for technical round"

    if score >= 5:
        return "Need more aptitude practice"

    return "Retake aptitude assessment"