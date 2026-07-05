def analyze_interview(score):

    if score >= 80:
        return {
            "status": "Excellent",
            "next_step":
            "Proceed to coding round"
        }

    elif score >= 60:
        return {
            "status": "Average",
            "next_step":
            "Practice technical concepts"
        }

    return {
        "status": "Poor",
        "next_step":
        "Restart HR interview"
    }