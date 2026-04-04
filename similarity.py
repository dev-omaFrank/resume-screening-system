from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, job_description_text):
    """
    Calculates the similarity between resume text and job description text
    using TF-IDF and cosine similarity.
    Returns the similarity score as a percentage (0-100%).
    """
    if not resume_text or not job_description_text:
        return 0.0

    documents = [resume_text, job_description_text]

    # Initialize TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # Calculate cosine similarity
    # The first document (resume) is compared with the second (job description)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # Convert to percentage
    return cosine_sim * 100
