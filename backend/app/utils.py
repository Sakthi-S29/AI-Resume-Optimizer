import re
from collections import Counter
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
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    matched = []
    missed = []

    for keyword in SKILL_KEYWORDS:
        if jd_keywords[keyword] > 0:
            if resume_keywords[keyword] > 0:
                matched.append(keyword)
            else:
                missed.append(keyword)

    match_score = len(matched) / (len(matched) + len(missed) + 1e-6)
    return {
        "score_percent": round(match_score * 100, 2),
        "matched_keywords": matched,
        "missing_keywords": missed
    }