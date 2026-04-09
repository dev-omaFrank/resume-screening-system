from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(resume_text, job_desc, top_n=5):
    # Split into sentences
    resume_sentences = [s.strip() for s in resume_text.split('.') if s.strip()]
    job_sentences = [s.strip() for s in job_desc.split('.') if s.strip()]
    
    # Encode all sentences
    resume_embeddings = model.encode(resume_sentences, convert_to_tensor=True)
    job_embeddings = model.encode(job_sentences, convert_to_tensor=True)
    
    # Compute similarity matrix
    similarity_matrix = util.cos_sim(job_embeddings, resume_embeddings)
    
    # For each job sentence → find best matching resume sentence
    best_scores = similarity_matrix.max(dim=1).values
    
    # Overall score = average best matches
    overall_similarity = float(best_scores.mean() * 100)
    
    # Get weakest job requirements (bad matches)
    worst_indices = best_scores.argsort()[:top_n]
    feedback = [job_sentences[i] for i in worst_indices]
    
    return {
        "similarity": overall_similarity,
        "feedback": feedback
    }