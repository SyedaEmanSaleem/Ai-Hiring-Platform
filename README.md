# 🤖 AI Hiring Platform

An end-to-end AI-powered recruitment platform built with **Python** and **Flask** that automates the hiring process—from resume screening to interview evaluation and hiring reports.

The platform can:

- 📄 Screen resumes against job requirements
- 🎯 Match candidate skills with job requirements
- ❓ Generate technical, behavioral, and skill-gap interview questions
- 💬 Conduct AI-assisted interviews
- 📊 Score candidate performance
- 📑 Generate detailed hiring reports
- 📈 Rank candidates on a recruiter dashboard

> **Works completely offline by default.** No OpenAI API key or paid services are required. You can optionally integrate any LLM (OpenAI, Gemini, Ollama, Claude, etc.) later.

---

# ✨ Features

- Resume Upload (`PDF`, `DOCX`, `TXT`)
- AI Resume Screening
- Skill & Experience Extraction
- Job Matching
- Automatic Interview Question Generation
- AI Interview Evaluation
- Candidate Scoring
- Hiring Recommendation
- Markdown Report Generation
- CSV Candidate Ranking
- Recruiter Dashboard
- SQLite Database Storage
- Offline Mode
- Optional LLM Support

---

# 🏗️ Project Structure

```text
ai-hiring-platform/
│
├── app.py                     # Flask Web Application
├── main.py                    # Command Line Version
├── db.py                      # SQLite Database
├── models.py                  # Candidate & Job Models
├── resume_screener.py         # Resume Screening Engine
├── file_reader.py             # PDF/DOCX/TXT Reader
├── question_generator.py      # Interview Question Generator
├── interview_conductor.py     # Interview Evaluation
├── candidate_scorer.py        # Final Candidate Scoring
├── report_generator.py        # Markdown & CSV Reports
├── llm_client.py              # Optional LLM Integration
├── requirements.txt
├── hiring_platform.db
│
├── templates/
├── static/
├── uploads/
└── hiring_reports/
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/SyedaEmanSaleem/ai-hiring-platform.git
cd ai-hiring-platform
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Start the Web Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 💻 Run the Terminal Version

```bash
python main.py
```

---

# 🌐 Web Application Workflow

### 1️⃣ Upload Resume

- Enter Job Title
- Required Skills
- Preferred Skills
- Minimum Experience
- Candidate Information
- Upload Resume (`PDF`, `DOCX`, `TXT`)

↓

### 2️⃣ Resume Screening

The system automatically:

- Extracts Skills
- Detects Experience
- Matches Skills
- Calculates Resume Score

↓

### 3️⃣ Interview

AI generates:

- Technical Questions
- Behavioral Questions
- Skill Gap Questions

Enter candidate responses directly in the browser.

↓

### 4️⃣ Candidate Evaluation

The platform evaluates:

- Resume Score
- Interview Performance
- Technical Knowledge
- Communication Quality

↓

### 5️⃣ Hiring Report

Generate:

- Final Score
- Hiring Recommendation
- Markdown Report
- Candidate Ranking

---

# 📊 Scoring Pipeline

```
Resume Upload
      │
      ▼
Resume Screening
      │
      ▼
Question Generation
      │
      ▼
Interview Evaluation
      │
      ▼
Final Candidate Score
      │
      ▼
Hiring Report
```

---

# 📂 Supported Resume Formats

- PDF
- DOCX
- TXT

---

# 📁 Generated Files

The application automatically creates:

```
uploads/
```

Uploaded resumes

```
hiring_reports/
```

- Candidate Markdown Reports
- Hiring Summary CSV

```
hiring_platform.db
```

SQLite Database

---

# 💾 Database

The application stores:

- Candidates
- Resume Scores
- Interview Questions
- Interview Answers
- Final Scores
- Hiring Recommendations

All data is stored locally using **SQLite**.

---

# 🧠 AI Features

- Resume Parsing
- Skill Extraction
- Experience Detection
- Candidate Ranking
- AI Interview Generation
- Interview Scoring
- Hiring Recommendation
- Automated Report Generation

---

# 🔌 Optional LLM Integration

The project includes **llm_client.py** for integrating:

- OpenAI GPT
- Google Gemini
- Ollama
- Anthropic Claude
- Azure OpenAI
- Any OpenAI-Compatible API

Simply implement `call_llm()` and enable:

```python
USE_LLM = True
```

The platform automatically switches from rule-based logic to LLM-powered evaluation.

---

# ⚙️ Customization

You can easily customize:

- Resume Scoring Formula
- Required Skills
- Interview Questions
- Candidate Ranking Logic
- Hiring Thresholds
- Recommendation Categories

---

# 📈 Dashboard

The dashboard provides:

- Candidate Rankings
- Resume Scores
- Interview Scores
- Final Scores
- Hiring Recommendations

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Flask | Web Framework |
| SQLite | Database |
| HTML5 | Frontend |
| CSS3 | Styling |
| Jinja2 | Templates |
| PyPDF | PDF Parsing |
| python-docx | DOCX Parsing |

---

# 🚀 Future Improvements

- User Authentication
- Recruiter Accounts
- PostgreSQL/MySQL Support
- Voice Interviews
- Video Interviews
- AI Resume Summarization
- Email Notifications
- Analytics Dashboard
- Docker Deployment
- REST API
- Multi-user Support
- Cloud Deployment

---

# 📸 Screenshots

Add screenshots here after deployment.

Example:

```
screenshots/home.png

screenshots/screening.png

screenshots/report.png

screenshots/dashboard.png
```

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add feature"
```

4. Push your branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Syeda Eman Saleem**

Built with ❤️ using **Python**, **Flask**, and **AI** to automate the recruitment process.

---

## ⭐ If you found this project helpful, don't forget to star the repository!
