import re

def extract_years_of_experience(ai_recommendation):
    """Extract years of experience from AI recommendation text."""
    if not ai_recommendation:
        return "N/A"
    
    # Pattern to match years of experience (e.g., "5 years", "5+ years", "5-7 years")
    patterns = [
        r'(\d+[\+]?\s*years?\s+of\s+experience)',
        r'(\d+[\-]\d+\s+years?\s+of\s+experience)',
        r'(excellent\s+years?\s+of\s+experience)',
        r'(good\s+years?\s+of\s+experience)',
        r'(moderate\s+years?\s+of\s+experience)',
        r'(limited\s+years?\s+of\s+experience)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, ai_recommendation, re.IGNORECASE)
        if match:
            return match.group(1).title()
    
    return "Not specified"


def extract_match_level(ai_recommendation):
    """Extract overall match level from AI recommendation."""
    if not ai_recommendation:
        return "N/A"
    
    # Pattern to match match level
    patterns = [
        r'(excellent\s+match)',
        r'(strong\s+match)',
        r'(good\s+match)',
        r'(fair\s+match)',
        r'(weak\s+match)',
        r'(poor\s+match)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, ai_recommendation, re.IGNORECASE)
        if match:
            return match.group(1).title()
    
    return "Not specified"


def extract_missing_skills(ai_recommendation):
    """Extract missing skills from AI recommendation."""
    if not ai_recommendation:
        return []
    
    # Pattern to match "Missing skills: skill1, skill2, skill3"
    pattern = r'Missing\s+skills?:\s*([^\n]+)'
    match = re.search(pattern, ai_recommendation, re.IGNORECASE)
    
    if match:
        skills_text = match.group(1)
        # Split by comma and clean up
        skills = [s.strip() for s in skills_text.split(',') if s.strip()]
        return skills
    
    return []


def get_matched_skills(submission):
    """Get matched skills (strengths that are NOT in missing skills)."""
    strengths_text = submission.get('strengths', '')
    gaps_text = submission.get('gaps', '')
    
    if not strengths_text:
        return []
    
    # Parse strengths (matched skills)
    matched = [s.strip().lower() for s in strengths_text.split(',') if s.strip()]
    
    if gaps_text:
        # Parse gaps (missing skills)
        missing = [s.strip().lower() for s in gaps_text.split(',') if s.strip()]
        
        # Filter out missing skills to get truly matched skills
        matched = [s for s in matched if s not in missing]
    
    return matched


def get_skill_summary(submission):
    """Get a summary of matched vs missing skills."""
    matched = get_matched_skills(submission)
    missing = extract_missing_skills(submission.get('ai_recommendation', ''))
    
    return {
        'matched_count': len(matched),
        'missing_count': len(missing),
        'matched': matched,
        'missing': missing
    }