import random

APTITUDE_QUESTIONS = [

    # QUANTITATIVE

    {
        "question": "What is 25% of 400?",
        "options": ["50", "75", "100", "125"],
        "answer": "100"
    },

    {
        "question": "If x+12=30, find x.",
        "options": ["18", "20", "15", "10"],
        "answer": "18"
    },

    {
        "question": "Find the next number: 2,4,8,16,?",
        "options": ["20", "24", "32", "64"],
        "answer": "32"
    },

    {
        "question": "A train travels 60 km in 2 hours. What is its speed?",
        "options": ["20", "30", "40", "50"],
        "answer": "30"
    },

    {
        "question": "What is 15 × 12?",
        "options": ["150", "170", "180", "200"],
        "answer": "180"
    },

    {
        "question": "Find 30% of 250.",
        "options": ["65", "70", "75", "80"],
        "answer": "75"
    },

    {
        "question": "A shop gives 20% discount on ₹500. Final price?",
        "options": ["350", "400", "450", "300"],
        "answer": "400"
    },

    {
        "question": "The average of 10,20,30 is?",
        "options": ["15", "20", "25", "30"],
        "answer": "20"
    },

    {
        "question": "What is the square root of 144?",
        "options": ["10", "12", "14", "16"],
        "answer": "12"
    },

    {
        "question": "Find 15% of 600.",
        "options": ["70", "80", "90", "100"],
        "answer": "90"
    },

    # LOGICAL

    {
        "question": "Odd one out: Apple, Mango, Carrot, Orange",
        "options": ["Apple", "Mango", "Carrot", "Orange"],
        "answer": "Carrot"
    },

    {
        "question": "Find next: 1,4,9,16,?",
        "options": ["20", "25", "30", "36"],
        "answer": "25"
    },

    {
        "question": "Which number is missing? 2,6,12,20,?",
        "options": ["28", "30", "32", "36"],
        "answer": "30"
    },

    {
        "question": "If SOUTH becomes HTUOS, NORTH becomes?",
        "options": ["HTRON", "NROTH", "HTRON", "NORTH"],
        "answer": "HTRON"
    },

    {
        "question": "If A>B and B>C, then?",
        "options": ["A<C", "A>C", "A=B", "None"],
        "answer": "A>C"
    },

    {
        "question": "Find next: 3,6,12,24,?",
        "options": ["36", "48", "50", "60"],
        "answer": "48"
    },

    # VERBAL

    {
        "question": "Choose the synonym of HAPPY.",
        "options": ["Sad", "Joyful", "Angry", "Fear"],
        "answer": "Joyful"
    },

    {
        "question": "Choose the antonym of FAST.",
        "options": ["Quick", "Rapid", "Slow", "Speed"],
        "answer": "Slow"
    },

    {
        "question": "Find the correct spelling.",
        "options": [
            "Accomodation",
            "Accommodation",
            "Acommodation",
            "Accomadation"
        ],
        "answer": "Accommodation"
    },

    {
        "question": "He ____ to school every day.",
        "options": ["go", "goes", "gone", "going"],
        "answer": "goes"
    },

    {
        "question": "Choose the synonym of BRAVE.",
        "options": ["Coward", "Bold", "Weak", "Lazy"],
        "answer": "Bold"
    },

    # DATA INTERPRETATION

    {
        "question": "If sales are 100,120,150, average sales?",
        "options": ["110", "120", "123.3", "130"],
        "answer": "123.3"
    },

    {
        "question": "A class has 40 students. 25 are boys. Girls?",
        "options": ["10", "15", "20", "25"],
        "answer": "15"
    },

    {
        "question": "Profit = ₹500, Cost = ₹2500. Profit %?",
        "options": ["10", "15", "20", "25"],
        "answer": "20"
    },

    {
        "question": "Simple interest on ₹1000 at 10% for 2 years?",
        "options": ["100", "150", "200", "250"],
        "answer": "200"
    },

    {
        "question": "A car covers 240 km in 4 hours. Speed?",
        "options": ["40", "50", "60", "70"],
        "answer": "60"
    },

    # ANALYTICAL

    {
        "question": "What comes after Z,Y,X,W?",
        "options": ["V", "U", "T", "S"],
        "answer": "V"
    },

    {
        "question": "How many sides does a hexagon have?",
        "options": ["4", "5", "6", "7"],
        "answer": "6"
    },

    {
        "question": "Binary of decimal 5?",
        "options": ["100", "101", "110", "111"],
        "answer": "101"
    }
]


def generate_aptitude_test():

    total_questions = min(
        20,
        len(APTITUDE_QUESTIONS)
    )

    return random.sample(
        APTITUDE_QUESTIONS,
        total_questions
    )