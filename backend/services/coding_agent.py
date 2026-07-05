def analyze_code(language, code):

    score = 50
    suggestions = []

    if "for" in code:
        score += 20

    if "function" in code or "def" in code:
        score += 20

    if len(code) > 100:
        score += 10

    if score < 70:
        suggestions.append(
            "Improve coding logic"
        )

    return score, suggestions