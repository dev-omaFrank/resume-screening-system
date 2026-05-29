# Add this NEW validation function

def validate_match_strict(resume_skills, job_skills, required_skills=None):
    """
    Validate match with stricter rules.
    
    Args:
        resume_skills: Skills found in resume
        job_skills: All skills required for job
        required_skills: MINIMUM required skills (must match at least X)
    
    Returns:
        dict: Validated match results
    """
    resume_skills_lower = set(s.lower().strip() for s in resume_skills)
    job_skills_lower = set(s.lower().strip() for s in job_skills)
    
    # 1. Check exact matches ONLY (no substrings)
    matched = []
    for job_skill in job_skills_lower:
        for resume_skill in resume_skills_lower:
            # Match whole word only, case-sensitive alternative
            if job_skill == resume_skill:
                matched.append(job_skill)
                break
    
    matched = list(set(matched))
    missing = list(job_skills_lower - set(matched))
    
    # 2. Calculate base percentage
    base_percentage = len(matched) / len(job_skills_lower) * 100 if job_skills_lower else 0
    
    # 3. ENFORCE minimum required skills
    if required_skills:
        required_lower = set(s.lower().strip() for s in required_skills)
        required_matched = resume_skills_lower.intersection(required_lower)
        
        # If less than 50% of required skills matched → FAIL
        required_match_rate = len(required_matched) / len(required_lower)
        if required_match_rate < 0.5:
            return {
                'matched': matched,
                'missing': missing,
                'match_percentage': 0,  # FAIL immediately
                'failed_reason': 'Insufficient required skills'
            }
    
    return {
        'matched': matched,
        'missing': missing,
        'match_percentage': round(base_percentage, 1),
        'failed_reason': None
    }
    
    
def generate_explanation(match_score, skills_match, experience_score, tfidf_score=None):
    """
    Generate AI recommendation explanation.

    Args:
        match_score: Overall match percentage
        skills_match: Dict with matched, missing, extra skills
        experience_score: Experience score percentage
        tfidf_score: TF-IDF similarity score (optional)

    Returns:
        str: Human-readable explanation
    """
    explanations = []
    
    # Match level
    if match_score >= 70:
        explanations.append("• Strong Match")
    elif match_score >= 50:
        explanations.append("• Moderate Match")
    else:
        explanations.append("• Weak Match")
        
    # Experience level
    if experience_score >= 80:
        explanations.append(f"• Candidate has very valid experience (Excellent)")
    elif experience_score >= 60:
        explanations.append(f"• Candidate possess good experience (Moderate)")
    elif experience_score >= 40:
        explanations.append(f"• Candidate has some experience in this field (Fair)")
    else:
        explanations.append(f"• Candidate has limited experience in this field (Poor)")

    # Matched skills
    if skills_match['matched']:
        explanations.append(f"<br>Candidate possesses the following skills: {'<br>•'.join(skills_match['matched'][:3])}")

    # Missing skills
    if skills_match['missing']:
        explanations.append(f"<br>Candidate lacks the following skills: {'<br>•'.join(skills_match['missing'][:3])}")

    return "<br>".join(explanations)

def get_status(match_score):
    """Get employment status based on score."""
    if match_score >= 70:
        return "Employable"
    elif match_score >= 50:
        return "Fair"
    else:
        return "Not employable"

def combine_scores(tfidf_score, skills_match_percentage, experience_score):
    """Combine all scores into final percentage."""
    final_score = (
        tfidf_score * 0.30 +           
        skills_match_percentage * 0.30 + 
        experience_score * 0.40          
    )
    return round(final_score, 2)