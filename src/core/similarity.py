# TF-IDF Similarity Calculation (FROZEN - DO NOT MODIFY)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_similarity(resume_text, job_description_text):
    """
    Calculate cosine similarity between resume and job description using TF-IDF.

    Args:
        resume_text: Preprocessed resume text
        job_description_text: Preprocessed job description text

    Returns:
        float: Similarity score as percentage (0-100)
    """
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return float(similarity[0][0] * 100)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0
