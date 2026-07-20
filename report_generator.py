"""
Hiring Report Generator
-------------------------
Produces a per-candidate Markdown report and a summary CSV ranking all
candidates for a given job requisition.
"""
import csv
import os
from datetime import datetime
from typing import List
from models import Candidate, JobRequirement


def generate_candidate_report(candidate: Candidate, job: JobRequirement) -> str:
    lines = []
    lines.append(f"# Hiring Report — {candidate.name}")
    lines.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")

    lines.append(f"**Role:** {job.title}")
    lines.append(f"**Candidate ID:** {candidate.candidate_id}")
    lines.append(f"**Email:** {candidate.email}\n")

    lines.append("## Summary")
    lines.append(f"- **Final Score:** {candidate.final_score}/100")
    lines.append(f"- **Recommendation:** {candidate.recommendation}")
    lines.append(f"- **Screening Score:** {candidate.screening_score}/100")
    lines.append(f"- **Interview Score:** {candidate.interview_score}/10\n")

    lines.append("## Resume Screening")
    lines.append(f"- Extracted skills: {', '.join(candidate.extracted_skills) or 'none detected'}")
    lines.append(f"- Experience: {candidate.experience_years} years")
    lines.append(f"- Education: {candidate.education}")
    for note in candidate.screening_notes:
        lines.append(f"- {note}")
    lines.append("")

    lines.append("## Interview Transcript & Scoring")
    for i, qa in enumerate(candidate.interview_qas, 1):
        lines.append(f"**Q{i} [{qa['category']}]:** {qa['question']}")
        lines.append(f"> {qa['answer'] or '(no answer provided)'}")
        lines.append(f"Score: {qa['score']}/10\n")

    lines.append("## Notes for Hiring Manager")
    if candidate.recommendation == "Strong Hire":
        lines.append("Candidate demonstrates strong alignment with role requirements "
                      "and performed well across interview questions. Recommend moving "
                      "to final-round / offer stage.")
    elif candidate.recommendation == "Hire":
        lines.append("Solid candidate with good overall fit. Recommend proceeding, "
                      "with attention to any flagged skill gaps above.")
    elif candidate.recommendation == "Maybe / Further Review":
        lines.append("Mixed signals — some gaps in required skills or interview depth. "
                      "Consider a follow-up technical round before deciding.")
    else:
        lines.append("Significant gaps versus role requirements and/or weak interview "
                      "performance. Not recommended to proceed at this time.")

    return "\n".join(lines)


def save_candidate_report(candidate: Candidate, job: JobRequirement, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    report_text = generate_candidate_report(candidate, job)
    path = os.path.join(output_dir, f"report_{candidate.candidate_id}.md")
    with open(path, "w") as f:
        f.write(report_text)
    return path


def save_summary_csv(candidates: List[Candidate], job: JobRequirement, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "hiring_summary.csv")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Rank", "Candidate ID", "Name", "Email", "Role",
            "Screening Score", "Interview Score", "Final Score", "Recommendation"
        ])
        ranked = sorted(candidates, key=lambda c: c.final_score, reverse=True)
        for rank, c in enumerate(ranked, 1):
            writer.writerow([
                rank, c.candidate_id, c.name, c.email, job.title,
                c.screening_score, c.interview_score, c.final_score, c.recommendation
            ])
    return path
