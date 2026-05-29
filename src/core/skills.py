# Skills Matching and Extraction
import re
from src.config.skills_data import ALL_SKILLS

# ==============================================
# FROZEN FUNCTIONS (KEEP AS IS)
# ==============================================

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


def extract_skills_strict(text, blocklist=None):
    """Extract skills using word boundary matching - stricter version.
    
    Args:
        text: Resume text to extract skills from
        blocklist: List of skills to exclude (common false positives)
    
    Returns:
        list: Found skills (exact matches only)
    """
    if blocklist is None:
        blocklist = {
            'bank', 'cash', 'loan', 'team', 'manage', 'excel', 
            'client', 'service', 'support', 'account', 'credit', 
            'record', 'report', 'data', 'word', 'mail',
            'file', 'note', 'time', 'fund', 'check', 'card', 'pay',
            'sale', 'item', 'run', 'end', 'key', 'set', 'type',
            'order', 'code', 'base', 'rate', 'view', 'post'
        }
    
    text_lower = text.lower()
    found_skills = []

    for skill in ALL_SKILLS:
        skill_lower = skill.lower()
        
        if skill_lower in blocklist:
            continue
            
        # Word boundaries - must be whole word, not substring
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


def validate_match_strict(resume_skills, job_skills, required_skills=None):
    """Validate match with stricter rules.
    
    Args:
        resume_skills: Skills found in resume
        job_skills: All skills required for job
        required_skills: Critical skills that must be present
    
    Returns:
        dict: Validated match results with 'matched', 'missing', 'match_percentage', 'failed_reason'
    """
    resume_skills_lower = set(s.lower().strip() for s in resume_skills)
    job_skills_lower = set(s.lower().strip() for s in job_skills)
    
    # Check exact matches ONLY (no substring matching)
    matched = []
    for job_skill in job_skills_lower:
        for resume_skill in resume_skills_lower:
            if job_skill == resume_skill:
                matched.append(job_skill)
                break
    
    matched = list(set(matched))
    missing = list(job_skills_lower - set(matched))
    
    # Calculate percentage
    base_percentage = len(matched) / len(job_skills_lower) * 100 if job_skills_lower else 0
    
    # ENFORCE minimum required skills
    if required_skills:
        required_lower = set(s.lower().strip() for s in required_skills)
        required_matched = resume_skills_lower.intersection(required_lower)
        
        required_match_rate = len(required_matched) / len(required_lower)
        if required_match_rate < 0.5:
            return {
                'matched': matched,
                'missing': missing,
                'match_percentage': 0,
                'failed_reason': 'Insufficient required skills'
            }
    
    return {
        'matched': matched,
        'missing': missing,
        'match_percentage': round(base_percentage, 1),
        'failed_reason': None
    }


def match_skills_strict(resume_text, job_skills, required_skills=None):
    """Complete skills matching pipeline with strict extraction + validation.
    
    Args:
        resume_text: Raw resume text
        job_skills: Skills required for the job
        required_skills: Critical skills that must be present
    
    Returns:
        dict: Match results with 'matched', 'missing', 'match_percentage', 'failed_reason'
    """
    # Step 1: Extract skills with word boundaries
    resume_skills = extract_skills_strict(resume_text)
    
    # Step 2: Validate matches strictly
    result = validate_match_strict(resume_skills, job_skills, required_skills)
    
    return result
