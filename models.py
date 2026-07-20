"""
Shared data models for the AI Hiring Platform.
"""
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class JobRequirement:
    title: str
    required_skills: List[str]
    preferred_skills: List[str] = field(default_factory=list)
    min_experience_years: float = 0
    education_level: str = "Bachelor's"
    description: str = ""


@dataclass
class Candidate:
    candidate_id: str
    name: str
    email: str
    resume_text: str

    # Filled in by ResumeScreener
    extracted_skills: List[str] = field(default_factory=list)
    experience_years: float = 0.0
    education: str = "Unknown"
    screening_score: float = 0.0
    screening_notes: List[str] = field(default_factory=list)

    # Filled in by InterviewConductor
    interview_qas: List[Dict] = field(default_factory=list)
    interview_score: float = 0.0

    # Filled in by CandidateScorer
    final_score: float = 0.0
    recommendation: str = ""
    status: str = "Applied"
