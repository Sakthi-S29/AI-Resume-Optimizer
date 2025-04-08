import re
import boto3
from datetime import datetime, timezone
import uuid
import json
from pathlib import Path
from collections import Counter
from decimal import Decimal
from boto3.dynamodb.conditions import Key

SKILL_FILE = Path(__file__).parent / "skills.json"

with open(SKILL_FILE, "r") as f:
    SKILL_MAP = json.load(f)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("resume-optimizer-data")

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

        # Load suggestions JSON
    suggestion_path = Path(__file__).parent / "keyword_suggestions.json"
    with open(suggestion_path, "r") as f:
        suggestion_data = json.load(f)

    # Build suggestions for missing keywords
    suggestions = {}
    for keyword in missing:
        if keyword in suggestion_data:
            suggestions[keyword] = suggestion_data[keyword]


    score = len(matched) / (len(matched) + len(missing) + 1e-6)
    return {
        "score_percent": round(score * 100, 2),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "suggestions": suggestions
    }

def extract_relevant_skills_from_jd(jd_text: str) -> set:
    jd_tokens = set(clean_text(jd_text).split())
    relevant_skills = set()

    for skill, synonyms in SKILL_MAP.items():
        if any(s in jd_tokens for s in synonyms):
            relevant_skills.add(skill)

    return relevant_skills

def store_score_in_dynamodb(user_id: str, resume_text: str, jd_text: str, score_result: dict):
    resume_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    item = {
        "user_id": user_id,
        "resume_id": resume_id,
        "timestamp": timestamp,
        "score_precent": Decimal(str(score_result["score_percent"])),
        "matched_keywords": score_result["matched_keywords"],
        "missing_keywords": score_result["missing_keywords"],
        "source": "manual"
    }

    table.put_item(Item=item)

def get_score_history(user_id: str):
    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id)   
    )

    items = response.get("Items", [])

    sorted_items = sorted(items, key=lambda x: x.get("timestamp", ""), reverse=True)

    return {
        "user_id": user_id,
        "history": sorted_items
    }