from typing import Optional
import re

def extract_experience(text: str) -> Optional[int]:
    text = text.lower()
    
    matches = []
    
    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
        "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
        "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "twenty": 20
    }
    
    # Numeric patterns
    numeric_patterns = [
        r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?)',
        r'over\s*(\d+)\s*(?:years?|yrs?)',
        r'minimum\s*(\d+)\s*(?:years?|yrs?)',
        r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
    ]
    
    # Word-based pattern
    word_pattern = r'\b(' + '|'.join(word_to_num.keys()) + r')\b\s*(?:years?|yrs?)'
    
    #  Extract numeric matches 
    for pattern in numeric_patterns:
        for match in re.findall(pattern, text):
            if isinstance(match, tuple):
                matches.append(int(match[-1]))
            else:
                matches.append(int(match))
    
    #  Extract word matches 
    for match in re.findall(word_pattern, text):
        matches.append(word_to_num[match])
    
    # Remove duplicates
    matches = list(set(matches))
    
    # Sanity filter
    matches = [m for m in matches if m <= 50]
    
    return max(matches) if matches else None



def calculate_experience_score(resume_exp: Optional[int], job_exp: Optional[int]):
    """
    Returns experience score and status metadata.
    """
    if resume_exp is None and job_exp is None:
        return {"score": 50, "status": "no_data"}

    if job_exp is None:
        return {"score": 100, "status": "no_requirement"}

    if resume_exp is None:
        return {"score": 0, "status": "missing_candidate_data"}

    if job_exp == 0:
        return {"score": 100, "status": "entry_level"}

    score = 100 if resume_exp >= job_exp else (resume_exp / job_exp) * 100
    return {"score": score, "status": "valid"}