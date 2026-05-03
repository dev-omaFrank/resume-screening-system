# Experience Extraction and Scoring (FROZEN - DO NOT MODIFY)
import re

def extract_years_of_experience(text):
    """Extract years of experience from resume text."""
    patterns = [
        r'(\d+)\+?\s*years?\s*of\s*experience',
        r'(\d+)\+?\s*years?\s*experience',
        r'experience:\s*(\d+)\+?\s*years?',
    ]

    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([int(m) for m in matches])

    return max(years) if years else 0

def score_experience(years, required_years=0):
    """Score experience based on required years."""
    if required_years == 0:
        return 100

    ratio = min(years / required_years, 1.5)
    return min(ratio * 100, 100)
