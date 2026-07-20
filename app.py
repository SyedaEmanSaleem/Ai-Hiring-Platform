"""
AI Hiring Platform — Web App
------------------------------
A simple Flask website: a hiring manager fills in job requirements, uploads
a candidate's resume, the app screens it, generates interview questions,
lets you fill in the candidate's answers, scores everything, and shows a
downloadable hiring report.

Run:
    python3 app.py
Then open:
    http://127.0.0.1:5000

Candidate data is stored in memory for this demo (a Python dict). Restarting
the server clears it. For real production use, swap CANDIDATES_DB for a
real database.
"""
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename

from models import Candidate, JobRequirement
from file_reader import extract_text_from_file
from resume_screener import screen_resume
from question_generator import generate_questions
from interview_conductor import conduct_interview
from candidate_scorer import compute_final_score, rank_candidates
from report_generator import save_candidate_report

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
REPORT_DIR = os.path.join(os.path.dirname(__file__), "hiring_reports")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}

# In-memory stores (demo only — replace with a DB for production)
CANDIDATES_DB = {}   # candidate_id -> Candidate
QUESTIONS_DB = {}    # candidate_id -> list of question dicts
JOBS_DB = {}         # candidate_id -> JobRequirement

DEFAULT_JOB = JobRequirement(
    title="Backend Software Engineer",
    required_skills=["python", "sql", "aws", "docker"],
    preferred_skills=["machine learning", "react"],
    min_experience_years=3,
)


@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html", job=DEFAULT_JOB)


@app.route("/screen", methods=["POST"])
def screen():
    file = request.files.get("resume")
    if not file or file.filename == "":
        flash("Please choose a resume file to upload.")
        return redirect(url_for("index"))

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        flash(f"Unsupported file type '{ext}'. Please upload a .pdf, .docx, or .txt file.")
        return redirect(url_for("index"))

    candidate_id = uuid.uuid4().hex[:8]
    filename = secure_filename(f"{candidate_id}{ext}")
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)

    try:
        resume_text = extract_text_from_file(filepath)
    except Exception as e:
        flash(f"Could not read resume file: {e}")
        return redirect(url_for("index"))

    if not resume_text.strip():
        flash("No readable text was found in that resume file.")
        return redirect(url_for("index"))

    job = JobRequirement(
        title=request.form.get("job_title", "").strip() or DEFAULT_JOB.title,
        required_skills=[s.strip() for s in request.form.get("required_skills", "").split(",") if s.strip()],
        preferred_skills=[s.strip() for s in request.form.get("preferred_skills", "").split(",") if s.strip()],
        min_experience_years=float(request.form.get("min_experience") or 0),
    )

    candidate = Candidate(
        candidate_id=candidate_id,
        name=request.form.get("name", "Unknown").strip(),
        email=request.form.get("email", "").strip(),
        resume_text=resume_text,
    )

    screen_resume(candidate, job)
    questions = generate_questions(candidate, job)

    CANDIDATES_DB[candidate_id] = candidate
    QUESTIONS_DB[candidate_id] = questions
    JOBS_DB[candidate_id] = job

    return render_template("interview.html", candidate=candidate, questions=questions)


@app.route("/interview/<candidate_id>", methods=["POST"])
def interview(candidate_id):
    candidate = CANDIDATES_DB.get(candidate_id)
    questions = QUESTIONS_DB.get(candidate_id)
    job = JOBS_DB.get(candidate_id)
    if not candidate or not questions or not job:
        flash("Candidate session not found — please start again.")
        return redirect(url_for("index"))

    answers = [request.form.get(f"answer_{i}", "") for i in range(len(questions))]
    conduct_interview(candidate, questions, interactive=False, preset_answers=answers)
    compute_final_score(candidate)
    save_candidate_report(candidate, job, REPORT_DIR)

    return redirect(url_for("view_report", candidate_id=candidate_id))


@app.route("/report/<candidate_id>", methods=["GET"])
def view_report(candidate_id):
    candidate = CANDIDATES_DB.get(candidate_id)
    if not candidate:
        flash("Report not found.")
        return redirect(url_for("dashboard"))
    return render_template("report.html", candidate=candidate)


@app.route("/report/<candidate_id>/download", methods=["GET"])
def download_report(candidate_id):
    path = os.path.join(REPORT_DIR, f"report_{candidate_id}.md")
    if not os.path.exists(path):
        flash("Report file not found.")
        return redirect(url_for("dashboard"))
    return send_file(path, as_attachment=True)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    evaluated = [c for c in CANDIDATES_DB.values() if c.status == "Evaluated"]
    ranked = rank_candidates(evaluated)
    return render_template("dashboard.html", candidates=ranked)


if __name__ == "__main__":
    app.run(debug=False, port=5000)
