from sentence_transformers import util
import re

def skill_match(resume_sentences, skills_dict, model, threshold=0.5):
    results = {}
    
    sentences = [s.strip() for s in re.split(r'[.\n•]', resume_sentences) if s.strip()]
    
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
    
    results = {}
    
    for category, skills in skills_dict.items():
        skill_embeddings = model.encode(skills, convert_to_tensor=True)
        
        similarity_matrix = util.cos_sim(sentence_embeddings, skill_embeddings)
        
        matched = []
        
        for i in range(len(sentences)):
            if similarity_matrix[i].max() > threshold:
                best_idx = similarity_matrix[i].argmax()
                matched.append(skills[best_idx])
                
        results[category] = list(set(matched))
        
    return results

def extract_job_skills(job_desc, skills_dict):
    job_desc = job_desc.lower()
    
    job_skills = {}
    
    for category, skills in skills_dict.items():
        found = []
        
        for skill in skills:
            if skill in job_desc:
                found.append
                
        job_skills[category] = list(set(found))
        
    return job_skills

def get_missing_skills(job_skills, resume_skills):
    missing = {}
    
    for category in job_skills:
        job_set = set(job_skills[category])
        resume_set = set(resume_skills.get(category, []))
        
        diff = job_set - resume_set
        
        if diff:
            missing[category] = list(diff)
            
    return missing