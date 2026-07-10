# AI Resume & Mock Interview Agent

An **AI-powered career preparation platform** that helps students and job seekers improve their resumes, analyze ATS compatibility, practice mock interviews, and receive personalized AI recommendations for placement readiness.

---

# 📌 Features

### 👤 User Authentication

* User Registration
* Secure Login
* Password Encryption using Flask-Bcrypt
* Logout

---

### 📄 Resume Analyzer

* Upload Resume (PDF/DOCX)
* Extract Skills
* Extract Education
* Extract Projects
* Extract Experience
* Extract Email & Phone Number
* Calculate ATS Score
* Recommend Job Roles
* Identify Missing Skills
* Display Resume Analysis Dashboard

---

### 🎤 AI Mock Interview

* Select Job Role
* AI-generated Interview Questions
* Submit Answers
* Automatic Evaluation
* Interview Score
* Performance Feedback
* AI Suggestions

---

### 🤖 AI Career Agent

The AI Career Agent monitors:

* Resume ATS Score
* Interview Performance
* Placement Readiness

It provides:

* Resume Improvement Suggestions
* Interview Practice Recommendations
* Career Guidance
* Placement Readiness Status

---

### 📊 Dashboard

* Resume Statistics
* ATS Score
* Interview Statistics
* AI Recommendations
* Profile Strength Chart
* Placement Readiness

---

## 🛠️ Technologies Used

### Programming Languages

* Python
* HTML5
* CSS3
* JavaScript
* SQL

### Web Framework

* Flask

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2
* Chart.js

### Backend

* Flask
* SQLAlchemy
* Flask-Login
* Flask-Bcrypt
* Flask-CORS

### Database

* SQLite

### Deployment

* Gunicorn
* Render
* GitHub

---

# 📚 Libraries Used

* Flask
* Flask-Login
* Flask-Bcrypt
* Flask-CORS
* SQLAlchemy
* NLTK
* PyPDF2
* python-docx
* Chart.js

---

# 🧠 Algorithms Used

## Resume Analysis

* Keyword Matching
* Regular Expression (Regex)
* Rule-Based Skill Extraction

## ATS Score Calculation

Weighted scoring based on:

* Skills
* Projects
* Education
* Experience
* Resume Completeness

## AI Career Agent

Rule-based Decision Making

Example:

* ATS Score < 60 → Resume Improvement
* Interview Score < 70 → Interview Practice
* Multiple Interviews Completed → Placement Ready

---

# 🏗️ Project Architecture

```
                 User
                   │
                   ▼
        HTML / CSS / JavaScript
                   │
                   ▼
             Flask Backend
                   │
      ┌────────────┼────────────┐
      │            │            │
      ▼            ▼            ▼
 Resume      Interview      AI Career
 Analyzer      Engine          Agent
      │            │            │
      └────────────┼────────────┘
                   │
                   ▼
              SQLite Database
                   │
                   ▼
          Dashboard & Reports
```

---

# 🔄 Workflow

### Step 1

User registers and logs into the application.

↓

### Step 2

Uploads Resume.

↓

### Step 3

Resume Analyzer extracts:

* Skills
* Projects
* Education
* Experience

↓

### Step 4

ATS Score is calculated.

↓

### Step 5

Recommended job roles are generated.

↓

### Step 6

User selects a job role.

↓

### Step 7

Mock Interview starts.

↓

### Step 8

User answers interview questions.

↓

### Step 9

AI evaluates answers.

↓

### Step 10

Dashboard displays:

* ATS Score
* Interview Score
* AI Recommendations
* Placement Readiness

---

# 📂 Project Structure

```
AI-Resume-Mock-Interview-Agent/

│
├── backend/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── uploads/
│   ├── static/
│   ├── app.py
│   ├── config.py
│   └── extensions.py
│
├── instance/
│
├── requirements.txt
├── run.py
├── Procfile
├── render.yaml
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/renusrijeyapandiyan/AI-Resume-Mock-Interview-Agent.git
```

Move into the project folder

```bash
cd AI-Resume-Mock-Interview-Agent
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python run.py
```

Application URL

```
http://127.0.0.1:5000
```

---

# 🌐 Deployment

The application can be deployed using **Render**.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn run:app
```

---

# 📸 Screenshots

* Login Page
* Register Page
* Dashboard
* Resume Upload
* Resume Analysis
* ATS Report
* Mock Interview
* Interview Report
* AI Career Agent

*(Add screenshots in this section after deployment.)*

---

# 🔮 Future Enhancements

* AI Voice Interview
* Resume & Job Description Matching
* Company-specific Interview Questions
* GPT-based Answer Evaluation
* Email Notifications
* Resume Builder
* Multi-language Support
* AI Learning Roadmap
* Recruiter Dashboard

---

# 👩‍💻 Author

**Renu Sri J**

* B.E. Computer Science Engineering (Artificial Intelligence & Machine Learning)
* V.S.B Engineering College
* GitHub: [https://github.com/renusrijeyapandiyan](https://github.com/renusrijeyapandiyan)

---

# 📄 License

This project is developed for **educational and academic purposes**. You are free to use, modify, and extend it for learning and research.
