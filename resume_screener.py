"""
Resume Screener
----------------
Extracts skills, experience and education from raw resume text and scores
the candidate against a JobRequirement.

No external NLP dependency is required (pure regex / keyword matching), so
this runs out of the box. Swap `extract_skills` for an LLM/NER call if you
want smarter extraction (see llm_client.py for the plug-in point).
"""
import re
from typing import List
from models import Candidate, JobRequirement

# A small default skills vocabulary. Extend this list (or load from a file)
# to widen what the screener can recognize.
SKILL_VOCABULARY = [
    "python", "java", "c++", "c#", "javascript", "typescript", "sql", "nosql",
    "django", "flask", "fastapi", "react", "angular", "vue", "node.js",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd",
    "machine learning", "deep learning", "nlp", "computer vision",
    "pandas", "numpy", "pytorch", "tensorflow", "scikit-learn",
    "data analysis", "data engineering", "etl", "spark", "hadoop",
    "rest api", "graphql", "microservices", "git", "agile", "scrum",
    "project management", "communication", "leadership", "problem solving",
    "excel", "power bi", "tableau", "html", "css",
]

EDUCATION_LEVELS = [
    ("phd", "PhD"),
    ("doctorate", "PhD"),
    ("master", "Master's"),
    ("m.sc", "Master's"),
    ("mba", "Master's"),
    ("bachelor", "Bachelor's"),
    ("b.sc", "Bachelor's"),
    ("b.tech", "Bachelor's"),
    ("associate degree", "Associate's"),
    ("diploma", "Diploma"),
]


def extract_skills(resume_text: str, vocabulary: List[str] = None) -> List[str]:
    text = resume_text.lower()
    vocab = vocabulary or SKILL_VOCABULARY
    found = []
    for skill in vocab:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)
    return found


def extract_experience_years(resume_text: str) -> float:
    """Looks for patterns like '5 years of experience' or '3+ yrs'."""
    text = resume_text.lower()
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|yrs)\b", text)
    if matches:
        return max(float(m) for m in matches)
    return 0.0


def extract_education(resume_text: str) -> str:
    text = resume_text.lower()
    for keyword, label in EDUCATION_LEVELS:
        if keyword in text:
            return label
    return "Unknown"


def score_against_job(candidate: Candidate, job: JobRequirement) -> None:
    """Mutates candidate in place: sets screening_score and notes."""
    notes = []
    skills_set = set(s.lower() for s in candidate.extracted_skills)
    required = set(s.lower() for s in job.required_skills)
    preferred = set(s.lower() for s in job.preferred_skills)

    matched_required = required & skills_set
    missing_required = required - skills_set
    matched_preferred = preferred & skills_set

    required_score = (len(matched_required) / len(required) * 60) if required else 60
    preferred_score = (len(matched_preferred) / len(preferred) * 20) if preferred else 20

    exp_ratio = min(candidate.experience_years / job.min_experience_years, 1.0) \
        if job.min_experience_years > 0 else 1.0
    experience_score = exp_ratio * 20

    total = round(required_score + preferred_score + experience_score, 1)

    notes.append(f"Matched required skills: {sorted(matched_required) or 'none'}")
    if missing_required:
        notes.append(f"Missing required skills: {sorted(missing_required)}")
    notes.append(f"Matched preferred skills: {sorted(matched_preferred) or 'none'}")
    notes.append(
        f"Experience: {candidate.experience_years} yrs "
        f"(required: {job.min_experience_years} yrs)"
    )

    candidate.screening_score = total
    candidate.screening_notes = notes


def screen_resume(candidate: Candidate, job: JobRequirement) -> Candidate:
    candidate.extracted_skills = extract_skills(candidate.resume_text)
    candidate.experience_years = extract_experience_years(candidate.resume_text)
    candidate.education = extract_education(candidate.resume_text)
    score_against_job(candidate, job)
    return candidate
