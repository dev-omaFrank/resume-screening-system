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
        explanations.append("Strong overall match with job requirements.")
    elif match_score >= 50:
        explanations.append("Moderate match with job requirements.")
    else:
        explanations.append("Weak match with job requirements.")

    if skills_match['matched']:
        explanations.append(f"Matched skills: {', '.join(skills_match['matched'][:5])}")

    if skills_match['missing']:
        explanations.append(f"Missing skills: {', '.join(skills_match['missing'][:5])}")

    return " ".join(explanations)

def get_status(match_score):
    """Get employment status based on score."""
    if match_score >= 70:
        return "Employable"
    elif match_score >= 50:
        return "Fair"
    else:
        return "Not employable"
