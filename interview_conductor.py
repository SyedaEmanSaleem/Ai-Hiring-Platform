"""
Interview Conductor
--------------------
Runs the interview: asks each generated question and records/scores the
candidate's answer.

Two modes:
  - interactive=True  -> asks via input() in the terminal (real use)
  - interactive=False -> takes answers from a pre-supplied dict (automation /
                          batch processing / demo)

Scoring is keyword-overlap + answer-substance based by default. Swap in
llm_client.call_llm for semantic scoring if USE_LLM is enabled.
"""
from typing import List, Dict, Optional
from models import Candidate
from llm_client import call_llm, USE_LLM


def _rule_based_score(answer: str, keywords: List[str]) -> float:
    """0-10 score based on keyword coverage and answer substance."""
    if not answer or not answer.strip():
        return 0.0

    answer_lower = answer.lower()
    length_score = min(len(answer.split()) / 40, 1.0) * 4  # up to 4 pts for depth

    if keywords:
        hits = sum(1 for kw in keywords if kw.lower() in answer_lower)
        keyword_score = (hits / len(keywords)) * 6  # up to 6 pts for relevance
    else:
        keyword_score = 6.0  # no keyword list (e.g. open-ended) -> don't penalize

    return round(min(length_score + keyword_score, 10.0), 1)


def _llm_score(question: str, answer: str) -> float:
    prompt = (
        f"Question: {question}\nCandidate answer: {answer}\n\n"
        "Score this answer from 0 to 10 for relevance, correctness and depth. "
        "Reply with ONLY the number."
    )
    text = call_llm(prompt)
    try:
        return max(0.0, min(10.0, float(text.strip())))
    except ValueError:
        return 5.0  # fallback if parsing fails


def score_answer(question: str, answer: str, keywords: List[str]) -> float:
    if USE_LLM:
        try:
            return _llm_score(question, answer)
        except Exception:
            pass
    return _rule_based_score(answer, keywords)


def conduct_interview(candidate: Candidate, questions: List[Dict],
                       interactive: bool = False,
                       preset_answers: Optional[List[str]] = None) -> Candidate:
    """
    Runs through `questions` for `candidate`, collecting + scoring answers.
    `preset_answers` (used when interactive=False) must align by index with
    `questions`; missing entries are treated as blank answers.
    """
    qas = []
    for i, q in enumerate(questions):
        if interactive:
            print(f"\n[{q['category'].upper()}] {q['question']}")
            answer = input("Candidate answer: ")
        else:
            answer = preset_answers[i] if preset_answers and i < len(preset_answers) else ""

        score = score_answer(q["question"], answer, q.get("keywords", []))
        qas.append({
            "category": q["category"],
            "question": q["question"],
            "answer": answer,
            "score": score,
        })

    candidate.interview_qas = qas
    candidate.interview_score = round(
        sum(qa["score"] for qa in qas) / len(qas), 1
    ) if qas else 0.0
    return candidate
