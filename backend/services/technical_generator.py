import random

def generate_technical_questions(role):

    questions = {

        "Software Developer": [

            {
                "question": "What is OOP?",
                "options": [
                    "Programming paradigm",
                    "Database",
                    "Operating System",
                    "Compiler"
                ],
                "answer": "Programming paradigm"
            },

            {
                "question": "Which language is used for web development?",
                "options": [
                    "Python",
                    "HTML",
                    "C",
                    "Assembly"
                ],
                "answer": "HTML"
            },

            {
                "question": "What is SQL?",
                "options": [
                    "Database language",
                    "Programming language",
                    "Operating system",
                    "Framework"
                ],
                "answer": "Database language"
            },

            {
                "question": "What is inheritance?",
                "options": [
                    "OOP concept",
                    "Database",
                    "API",
                    "Algorithm"
                ],
                "answer": "OOP concept"
            },

            {
                "question": "What is a class?",
                "options": [
                    "Blueprint of object",
                    "Function",
                    "Variable",
                    "Loop"
                ],
                "answer": "Blueprint of object"
            }

        ]
    }

    return questions.get(
        role,
        questions["Software Developer"]
    )