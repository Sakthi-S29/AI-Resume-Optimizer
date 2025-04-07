import re
import json
from pathlib import Path
from collections import Counter
SKILL_FILE = Path(__file__).parent / "skills.json"

with open(SKILL_FILE, "r") as f:
    SKILL_MAP = json.load(f)

print(f"🔍 Skill map contains {len(SKILL_MAP)} skills")
print(f"🔍 Sample keys: {list(SKILL_MAP.keys())[:5]}")

SKILL_KEYWORDS = [
    "python", "java", "aws", "docker", "kubernetes", "git", "linux",
    "react", "node.js", "sql", "mongodb", "lambda", "dynamodb",
    "api", "cloud", "agile", "s3", "ci/cd", "rest", "html", "css"
]

def clean_text(text: str) -> str:
    text = text.replace("\n", " ")     
    text = text.replace("\t", " ")
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\bn(\w+)\b", r"\1", text)
    return text.strip()

def extract_keywords(text: str) -> Counter:
    cleaned = clean_text(text)
    tokens = cleaned.split()
    return Counter(tokens)

def score_resume_against_jd(resume_text: str, jd_text: str) -> dict:
    resume_tokens = set(clean_text(resume_text).split())
    relevant_skills = extract_relevant_skills_from_jd(jd_text)

    matched = []
    missing = []

    for skill in relevant_skills:
        synonyms = SKILL_MAP.get(skill, [])
        if any(s in resume_tokens for s in synonyms):
            matched.append(skill)
        else:
            missing.append(skill)

    print(f"🧠 Relevant skills from JD: {relevant_skills}")


    score = len(matched) / (len(matched) + len(missing) + 1e-6)
    return {
        "score_percent": round(score * 100, 2),
        "matched_keywords": matched,
        "missing_keywords": missing
    }

def extract_relevant_skills_from_jd(jd_text: str) -> set:
    jd_tokens = set(clean_text(jd_text).split())
    relevant_skills = set()

    for skill, synonyms in SKILL_MAP.items():
        if any(s in jd_tokens for s in synonyms):
            relevant_skills.add(skill)

    return relevant_skills