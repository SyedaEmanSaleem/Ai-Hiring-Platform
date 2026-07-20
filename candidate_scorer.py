"""
Candidate Scorer
-----------------
Combines resume-screening score and interview score into a final weighted
score, and assigns a hiring recommendation tier.
"""
from models import Candidate

# Weights must sum to 1.0
SCREENING_WEIGHT = 0.4
INTERVIEW_WEIGHT = 0.6

RECOMMENDATION_TIERS = [
    (85, "Strong Hire"),
    (70, "Hire"),
    (55, "Maybe / Further Review"),
    (0, "No Hire"),
]


def compute_final_score(candidate: Candidate) -> Candidate:
    # interview_score is on a 0-10 scale -> normalize to 0-100
    interview_pct = candidate.interview_score * 10
    final = (candidate.screening_score * SCREENING_WEIGHT) + (interview_pct * INTERVIEW_WEIGHT)
    candidate.final_score = round(final, 1)

    for threshold, label in RECOMMENDATION_TIERS:
        if candidate.final_score >= threshold:
            candidate.recommendation = label
            break

    candidate.status = "Evaluated"
    return candidate


def rank_candidates(candidates):
    return sorted(candidates, key=lambda c: c.final_score, reverse=True)
