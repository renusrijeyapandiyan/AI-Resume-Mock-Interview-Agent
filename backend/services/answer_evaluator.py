def evaluate_aptitude(
        correct_answer,
        user_answer):

    if not user_answer:

        return {
            "score": 0,
            "feedback": "Not answered"
        }

    if str(user_answer).strip().lower() == \
       str(correct_answer).strip().lower():

        return {
            "score": 100,
            "feedback": "Correct"
        }

    return {
        "score": 0,
        "feedback": "Incorrect"
    }