# Explanation Generation (FROZEN - DO NOT MODIFY)

def generate_explanation(match_score, skills_match, experience_score):
    """
    Generate AI recommendation explanation.

    Args:
        match_score: Overall match percentage
        skills_match: Dict with matched, missing, extra skills
        experience_score: Experience score percentage

    Returns:
        str: Human-readable explanation
    """
    explanations = []

    if match_score >= 70:
        explanations.append("• Strong match")
    elif match_score >= 50:
        explanations.append("• Moderate match")
    else:
        explanations.append("• Weak match\n")
        
    if experience_score >= 80:
        explanations.append("• Excellent years of experience")
    elif experience_score >= 60:
        explanations.append("• Good years of experience")
    elif experience_score >= 40:
        explanations.append("• Fair years of experience")
    else:
        explanations.append("• Limited years of experience")

    # if skills_match['matched']:
        # explanations.append(f"Matched skills: {', '.join(skills_match['matched'][:3])}")

    if skills_match['missing']:
        explanations.append(f"Missing skills: {', '.join(skills_match['missing'][:3])}")

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