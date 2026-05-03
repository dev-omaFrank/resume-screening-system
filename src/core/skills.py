# Skills Matching and Extraction (FROZEN - DO NOT MODIFY)
import re
from src.config.skills_data import ALL_SKILLS

def extract_skills(text):
    """Extract skills from text based on skills dictionary."""
    text_lower = text.lower()
    found_skills = []

    for skill in ALL_SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills

def match_skills(resume_skills, job_skills):
    """Match skills between resume and job description."""
    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))
    extra = list(set(resume_skills) - set(job_skills))

    return {
        'matched': matched,
        'missing': missing,
        'extra': extra,
        'match_percentage': len(matched) / len(job_skills) * 100 if job_skills else 0
    }
