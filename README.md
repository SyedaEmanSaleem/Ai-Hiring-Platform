```markdown
# AI Hiring Platform

An end-to-end AI-powered hiring pipeline that automatically:
1. **Screens resumes** against a job's requirements
2. **Generates interview questions** (technical, skill-gap, behavioral)
3. **Conducts AI interviews**
4. **Scores candidates**
5. **Generates hiring reports** (Markdown per candidate + summary CSV ranking)

Two ways to use it:
- **`app.py`** — a website: a hiring manager fills in the job, uploads a resume (PDF/DOCX/TXT), fills in the candidate's interview answers in the browser, and gets a scored report instantly. **This is what most people want.**
- **`main.py`** — a terminal/script version for batch processing or automation.

No external API key or paid service is required — it runs fully offline using keyword/rule-based logic. There's an optional plug-in point to use a real LLM for smarter question generation and answer scoring.

Candidate data is persisted to a local **SQLite database** (`hiring_platform.db`), so nothing is lost when you restart the server.

## 🌐 Run the website (recommended)

```bash
git clone <this-repo-url>
cd ai-hiring-platform
pip3 install -r requirements.txt --break-system-packages   # omit the flag on Windows/Mac
python3 app.py
```
Then open **http://127.0.0.1:5000** in your browser.

Flow:
1. Fill in the job title + required/preferred skills → upload a resume file (`.pdf`, `.docx`, or `.txt`) → click **Upload & Screen Resume**.
2. You'll see the screening results plus a generated interview question set. Type in the candidate's answers (from a real interview call, or typed live during one) → click **Submit Interview & Generate Report**.
3. You'll land on a full hiring report with the final score and recommendation, plus a **Download report (.md)** link.
4. Visit **Dashboard** (top-right) any time to see every candidate ranked side by side — this data survives server restarts.

## Project structure
```
ai-hiring-platform/
├── app.py                   # 🌐 Flask website (run this for the UI)
├── main.py                  # Terminal/script pipeline (batch/demo use)
├── db.py                    # SQLite persistence layer
├── models.py                # Candidate & JobRequirement data classes
├── resume_screener.py       # Skill/experience/education extraction + scoring
├── file_reader.py           # Extracts text from uploaded PDF/DOCX/TXT resumes
├── question_generator.py    # Builds tailored interview question sets
├── interview_conductor.py   # Runs the interview, scores answers
├── candidate_scorer.py      # Combines scores into a final recommendation
├── report_generator.py      # Markdown reports + CSV summary
├── llm_client.py            # Optional LLM plug-in (disabled by default)
├── templates/                # HTML pages for the website
├── uploads/                   # Uploaded resume files land here
├── requirements.txt
├── hiring_platform.db        # SQLite database (created automatically)
└── hiring_reports/          # Generated reports (created automatically)
```

## Quick start (terminal/script version)
```bash
cd ai-hiring-platform
python3 main.py
```
This runs a self-contained demo with two sample candidates and prints progress to the terminal, then writes reports to `./hiring_reports/`.

## Using it for real candidates

### Option A: Use the website
Just run `python3 app.py` and go through the upload → screen → interview → report flow in the browser. This is the easiest path for non-technical users.

### Option B: Edit `main.py`
Replace the `JOB` and `CANDIDATES` list at the top of `main.py` with your real job requirements and resume text. Set `INTERACTIVE = True` to type interview answers live in the terminal instead of using pre-supplied demo answers.

### Option C: Import the modules in your own script
```python
from models import Candidate, JobRequirement
from resume_screener import screen_resume
from question_generator import generate_questions
from interview_conductor import conduct_interview
from candidate_scorer import compute_final_score
from report_generator import save_candidate_report

job = JobRequirement(
    title="Data Analyst",
    required_skills=["sql", "excel", "python"],
    preferred_skills=["tableau", "power bi"],
    min_experience_years=2,
)

candidate = Candidate(
    candidate_id="C100",
    name="Jane Doe",
    email="jane@example.com",
    resume_text=open("resumes/jane_doe.txt").read(),
)

screen_resume(candidate, job)
questions = generate_questions(candidate, job)
conduct_interview(candidate, questions, interactive=True)
compute_final_score(candidate)
save_candidate_report(candidate, job, "./hiring_reports")
```

### Reading resumes from PDF/DOCX
The website (`app.py`) handles this automatically via `file_reader.py`. If you're using `main.py` or your own script, extract the text first:
```bash
pip install pypdf python-docx
```
```python
from pypdf import PdfReader
text = "\n".join(p.extract_text() for p in PdfReader("resume.pdf").pages)
```

## Data storage
Candidates, their screening results, generated questions, and interview answers are all stored in `hiring_platform.db` (SQLite), created automatically on first run. To start fresh, just delete this file — a new empty database will be created the next time the app starts.

## Customizing scoring & questions
- **Skill vocabulary**: edit `SKILL_VOCABULARY` in `resume_screener.py`.
- **Screening weight formula**: edit `score_against_job()` in `resume_screener.py` (currently 60% required skills / 20% preferred skills / 20% experience).
- **Question bank**: edit `TECHNICAL_BANK` and `BEHAVIORAL_BANK` in `question_generator.py` to add questions for more skills/roles.
- **Final weighting**: edit `SCREENING_WEIGHT` / `INTERVIEW_WEIGHT` in `candidate_scorer.py` (currently 40% screening / 60% interview).
- **Recommendation thresholds**: edit `RECOMMENDATION_TIERS` in `candidate_scorer.py`.

## Upgrading to a real LLM (optional)
By default everything runs on rule-based logic so it works with zero setup. To use an LLM for more natural question generation and semantic answer scoring:
1. Open `llm_client.py`.
2. Implement `call_llm()` with your provider's SDK (an example is sketched in the comments).
3. Set `USE_LLM = True` at the top of `llm_client.py`.

`question_generator.py` and `interview_conductor.py` will automatically use the LLM path when available, falling back to rule-based logic if the call fails.

## Going to production
If you want to actually deploy this for real hiring use beyond local testing, consider:
- Switching from SQLite to Postgres/MySQL for a multi-user, higher-volume deployment.
- Running it with a production server instead of Flask's dev server, e.g. `pip install gunicorn && gunicorn app:app`.
- Adding login/authentication so only your hiring team can access it.
- Storing uploaded resumes securely and defining a data-retention policy.
- Reviewing applicable employment/hiring-law requirements in your jurisdiction around automated candidate scoring and decision-making.

## Notes
- This is a starter/reference implementation meant to be extended — the resume parsing and scoring logic are intentionally simple and transparent so you can see and adjust exactly how scores are computed.
- For production use with real candidate data, add authentication and review any applicable employment/hiring-law compliance requirements (e.g. around automated decision-making in hiring) for your jurisdiction.

## License
MIT (or update to whatever license you'd like to use)
```

