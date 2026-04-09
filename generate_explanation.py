def generate_explanation(skills_found, missing_skills, match_score, exp_score, exp_used=True, thresholds=None):
    """
    Generate a strengths/gaps explanation for a resume.
    
    Parameters:
    - exp_used: Whether experience was factored into scoring (False for jobs with no requirement)
    """
    
    if thresholds is None:
        thresholds = {"similarity": 0.6, "experience": 0.5}
        
    explanation = {"strengths": [], "gaps": []}
    
    for category, skills in skills_found.items():
        if skills:
            explanation["strengths"].append(f"Strong in {category.replace('_', ' ').title()}: {', '.join(skills)}")
    
    for category, skills in missing_skills.items():
        if skills:
            explanation["gaps"].append(f"Missing {category.replace('_', ' ').title()}: {', '.join(skills)}")
    
    if match_score >= thresholds["similarity"]:
        explanation["strengths"].append(f"Resume closely matches job description (Similarity: {match_score:.2f})")
    else:
        explanation["gaps"].append(f"Resume has low match to job description (Similarity: {match_score:.2f})")
        
    # Only show experience message if it was actually used in scoring
    if exp_used:
        if exp_score >= thresholds["experience"]:
            explanation["strengths"].append(f"Experience meets job requirements")
        else:
            explanation["gaps"].append(f"❌ Experience does not fully meet job requirements ")
    # If exp_used is False, don't mention experience at all
    
    return explanation