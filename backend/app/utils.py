import re
import json
from pathlib import Path
from collections import Counter
SKILL_FILE = Path(__file__).parent / "skills.json"

with open(SKILL_FILE, "r") as f:
    SKILL_MAP = json.load(f)

SKILL_KEYWORDS = [
    "python", "java", "aws", "docker", "kubernetes", "git", "linux",
    "react", "node.js", "sql", "mongodb", "lambda", "dynamodb",
    "api", "cloud", "agile", "s3", "ci/cd", "rest", "html", "css"
]

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]"," ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_keywords(text: str) -> Counter:
    cleaned = clean_text(text)
    tokens = cleaned.split()
    return Counter(tokens)

def score_resume_against_jd(resume_text: str, jd_text: str) -> dict:
    resume_tokens = set(clean_text(resume_text).split())
    jd_tokens = set(clean_text(jd_text).split())

    matched = []
    missing = []

    for skill, synonyms in SKILL_MAP.items():
        if any(s in jd_tokens for s in synonyms):
            if any(s in resume_tokens for s in synonyms):
                matched.append(skill)
            else:
                missing.append(skill)

    match_score = len(matched) / (len(matched) + len(missing) + 1e-6)
    return {
        "score_percent": round(match_score * 100, 2),
        "matched_keywords": matched,
        "missing_keywords": missing
    }