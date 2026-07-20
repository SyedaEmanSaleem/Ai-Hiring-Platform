"""
Interview Question Generator
-----------------------------
Builds a tailored question set per candidate: role-specific technical
questions, gap-probing questions (for missing required skills), and a fixed
set of behavioral questions. Each question carries a list of `keywords`
used later by the InterviewConductor for basic answer scoring.
"""
from typing import List, Dict
from models import Candidate, JobRequirement
from llm_client import call_llm, USE_LLM

TECHNICAL_BANK = {
    "python": {
        "q": "Explain the difference between a list and a tuple in Python, and when you'd use each.",
        "keywords": ["mutable", "immutable", "list", "tuple", "performance"],
    },
    "sql": {
        "q": "Write/describe a SQL query to find the second-highest salary in an Employees table.",
        "keywords": ["subquery", "limit", "offset", "order by", "max", "distinct"],
    },
    "machine learning": {
        "q": "How would you handle an imbalanced dataset in a classification problem?",
        "keywords": ["oversampling", "undersampling", "smote", "class weight", "precision", "recall", "f1"],
    },
    "aws": {
        "q": "Describe how you'd design a scalable, fault-tolerant web service on AWS.",
        "keywords": ["load balancer", "auto scaling", "ec2", "s3", "rds", "availability zone", "redundancy"],
    },
    "react": {
        "q": "Explain the React component lifecycle and how hooks changed it.",
        "keywords": ["useeffect", "usestate", "lifecycle", "render", "hooks", "mount", "unmount"],
    },
    "docker": {
        "q": "What's the difference between a Docker image and a container, and how do you optimize image size?",
        "keywords": ["image", "container", "layer", "multi-stage", "cache", "dockerfile"],
    },
    "project management": {
        "q": "Walk through how you'd manage scope creep on a project with a fixed deadline.",
        "keywords": ["scope", "stakeholder", "prioritize", "timeline", "communication", "trade-off"],
    },
}

BEHAVIORAL_BANK = [
    {
        "q": "Tell me about a time you disagreed with a teammate or manager. How did you handle it?",
        "keywords": ["listen", "compromise", "communicat", "resolve", "respect", "feedback"],
    },
    {
        "q": "Describe a project that failed or fell short. What did you learn?",
        "keywords": ["learn", "mistake", "root cause", "improve", "accountab", "reflect"],
    },
    {
        "q": "How do you prioritize when you have multiple deadlines at once?",
        "keywords": ["priorit", "urgent", "important", "plan", "deadline", "communicate"],
    },
    {
        "q": "Tell me about a time you had to learn a new skill or tool quickly.",
        "keywords": ["learn", "research", "practice", "adapt", "resource", "documentation"],
    },
]

GAP_QUESTION_TEMPLATE = (
    "I didn't see '{skill}' clearly demonstrated in your resume, but it's important "
    "for this role. Can you describe your experience with it, if any?"
)


def _llm_generate_role_questions(job: JobRequirement, n: int = 3) -> List[Dict]:
    prompt = (
        f"Generate {n} interview questions (technical, role-specific) for a "
        f"'{job.title}' position requiring skills: {', '.join(job.required_skills)}. "
        f"Return one question per line, no numbering."
    )
    text = call_llm(prompt)
    lines = [l.strip("- ").strip() for l in text.splitlines() if l.strip()]
    return [{"category": "technical", "question": q, "keywords": []} for q in lines[:n]]


def generate_questions(candidate: Candidate, job: JobRequirement,
                        num_technical: int = 3, num_behavioral: int = 2) -> List[Dict]:
    questions: List[Dict] = []

    if USE_LLM:
        try:
            questions.extend(_llm_generate_role_questions(job, num_technical))
        except Exception:
            pass  # fall through to rule-based bank below

    if not questions:
        # Prefer questions tied to the job's required skills, in order.
        picked = 0
        for skill in job.required_skills:
            key = skill.lower()
            if key in TECHNICAL_BANK and picked < num_technical:
                item = TECHNICAL_BANK[key]
                questions.append({
                    "category": "technical",
                    "question": item["q"],
                    "keywords": item["keywords"],
                })
                picked += 1

        # Gap-probing questions for missing required skills not covered above.
        candidate_skills = set(s.lower() for s in candidate.extracted_skills)
        missing = [s for s in job.required_skills if s.lower() not in candidate_skills]
        for skill in missing:
            if picked >= num_technical:
                break
            questions.append({
                "category": "gap_check",
                "question": GAP_QUESTION_TEMPLATE.format(skill=skill),
                "keywords": [skill.lower()],
            })
            picked += 1

    # Behavioral questions (fixed rotation, deterministic by candidate id length)
    start = len(candidate.candidate_id) % len(BEHAVIORAL_BANK)
    for i in range(num_behavioral):
        item = BEHAVIORAL_BANK[(start + i) % len(BEHAVIORAL_BANK)]
        questions.append({
            "category": "behavioral",
            "question": item["q"],
            "keywords": item["keywords"],
        })

    return questions
