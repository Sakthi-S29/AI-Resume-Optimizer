from typing import List, Dict

def generate_resume(name: str, email: str, skills: List[str], projects: List[Dict], education: str, certifications: List[str]):
    resume = {
        "header": {
            "name": name,
            "email": email,
        },
        "skills": skills,
        "education": education,
        "certifications": certifications,
        "projects": []
    }

    for project in projects:
        title = project.get("title", "Untitled Project")
        star = {
            "title": title,
            "situation": project.get("situation", ""),
            "task": project.get("task", ""),
            "action": project.get("action", ""),
            "result": project.get("result", "")
        }
        resume["projects"].append(star)

    return resume
