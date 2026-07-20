"""
AI Hiring Platform — Main Pipeline
------------------------------------
Runs the full flow end to end:
  1. Screen resumes         (resume_screener.py)
  2. Generate questions      (question_generator.py)
  3. Conduct AI interview    (interview_conductor.py)
  4. Score candidates        (candidate_scorer.py)
  5. Generate hiring reports (report_generator.py)

Run:
    python main.py

By default this runs a self-contained DEMO with sample resumes and
pre-supplied interview answers, so you can see the whole pipeline work with
zero setup. To use it for real candidates, either:
  - Edit the `CANDIDATES` list below with real resume text, and run in
    interactive mode (set INTERACTIVE = True) to type answers live, or
  - Import the modules directly in your own script (see README.md).
"""
import os
from models import Candidate, JobRequirement
from resume_screener import screen_resume
from question_generator import generate_questions
from interview_conductor import conduct_interview
from candidate_scorer import compute_final_score, rank_candidates
from report_generator import save_candidate_report, save_summary_csv

OUTPUT_DIR = "./hiring_reports"
INTERACTIVE = False  # True = type answers live in terminal; False = use demo answers below


# ---------------------------------------------------------------------------
# Demo data — replace with real job + candidates for actual use
# ---------------------------------------------------------------------------

JOB = JobRequirement(
    title="Backend Software Engineer",
    required_skills=["python", "sql", "aws", "docker"],
    preferred_skills=["machine learning", "react"],
    min_experience_years=3,
    education_level="Bachelor's",
    description="Build and scale backend services for our platform.",
)

CANDIDATES = [
    Candidate(
        candidate_id="C001",
        name="Ayesha Khan",
        email="ayesha.khan@example.com",
        resume_text="""
            Ayesha Khan — Software Engineer
            5 years of experience building backend systems with Python, Django, and SQL.
            Deployed services on AWS using Docker and CI/CD pipelines.
            Bachelor's degree in Computer Science.
        """,
    ),
    Candidate(
        candidate_id="C002",
        name="Bilal Ahmed",
        email="bilal.ahmed@example.com",
        resume_text="""
            Bilal Ahmed — Junior Developer
            1 year of experience with Python and basic SQL.
            Familiar with Git and Agile workflows. No cloud experience yet.
            Bachelor's degree in Information Technology.
        """,
    ),
]

# Pre-supplied demo answers, keyed by candidate_id, aligned by question index.
# In INTERACTIVE mode these are ignored and you'll be prompted live instead.
DEMO_ANSWERS = {
    "C001": [
        "Lists are mutable and can change size, tuples are immutable and faster "
        "to iterate over; I use tuples for fixed data like coordinates.",
        "You could use a subquery with LIMIT and OFFSET, or DISTINCT combined "
        "with ORDER BY salary DESC to skip the top value.",
        "I designed an auto-scaling group behind a load balancer across multiple "
        "availability zones, with RDS for persistence and S3 for static assets.",
        "On a project last year my manager and I disagreed on architecture; "
        "I proposed a proof of concept and we compromised on a hybrid approach "
        "after reviewing it together.",
        "A rollout once failed because of a missed edge case; I learned to "
        "always add a rollback plan and better test coverage.",
    ],
    "C002": [
        "I don't have direct AWS experience, but I understand EC2 hosts servers "
        "and S3 is for storage. I'm eager to learn cloud infrastructure.",
        "A subquery could find it, but I'd need to look up the exact syntax.",
        "I haven't used Docker in production yet, mostly followed tutorials.",
        "I prioritize by asking my manager which deadline matters most and "
        "focus there first.",
        "I once had to learn React quickly for a class project by following "
        "the official docs and building small examples.",
    ],
}


def run_pipeline():
    print(f"=== AI Hiring Platform: {JOB.title} ===\n")
    evaluated = []

    for candidate in CANDIDATES:
        print(f"--- Processing {candidate.name} ({candidate.candidate_id}) ---")

        # 1. Screen resume
        screen_resume(candidate, JOB)
        print(f"Screening score: {candidate.screening_score}/100")

        # 2. Generate interview questions
        questions = generate_questions(candidate, JOB)

        # 3. Conduct interview
        preset = DEMO_ANSWERS.get(candidate.candidate_id, [])
        conduct_interview(candidate, questions, interactive=INTERACTIVE, preset_answers=preset)
        print(f"Interview score: {candidate.interview_score}/10")

        # 4. Score candidate
        compute_final_score(candidate)
        print(f"Final score: {candidate.final_score}/100 -> {candidate.recommendation}\n")

        evaluated.append(candidate)

    # 5. Generate hiring reports
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for candidate in evaluated:
        path = save_candidate_report(candidate, JOB, OUTPUT_DIR)
        print(f"Report saved: {path}")

    summary_path = save_summary_csv(evaluated, JOB, OUTPUT_DIR)
    print(f"Summary CSV saved: {summary_path}")

    print("\n=== Final Ranking ===")
    for rank, c in enumerate(rank_candidates(evaluated), 1):
        print(f"{rank}. {c.name} — {c.final_score}/100 — {c.recommendation}")


if __name__ == "__main__":
    run_pipeline()
