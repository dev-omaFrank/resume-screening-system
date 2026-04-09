import streamlit as st
from skills import skill_match, extract_job_skills, get_missing_skills
from resume_parser import extract_text_from_pdf
from banking_skills import BANKING_SKILLS
from similarity import calculate_similarity
from experience import extract_experience, calculate_experience_score
from cleaning import anonymize_resume
from generate_explanation import generate_explanation
from text_extractor import extract_text

st.set_page_config(page_title="AI Resume Screening System")

@st.cache_resource
def load_model():
    from similarity import model as loaded_model
    return loaded_model

model = load_model()

st.title("AI Resume Screening System")
st.markdown("Upload one or more resumes and paste a job description to get match scores.")

# Job Description Input
st.header("1. Job Description")
job_description = st.text_area("Paste the Job Description here:", height=200)

# Resume Upload
st.header("2. Upload Resume(s)")
uploaded_files = st.file_uploader(
    "Choose one or more resume files", 
    type=["pdf", "txt", "docx"], 
    accept_multiple_files=True
)

gender = st.selectbox('Please select your gender', ['Male', 'Female'])

age = st.number_input("Enter your age", value=None, placeholder="Enter your age", format="%d", step=1)

if st.button("Evaluate Match"):
    if uploaded_files and job_description and gender and age:
        for uploaded_file in uploaded_files:
            st.header(f"Processing: {uploaded_file.name}")

            # --- Extract text ---
            with st.spinner("Extracting text from resume..."):
                resume_text = extract_text(uploaded_file)
                if resume_text:
                    resume_text = anonymize_resume(resume_text)
                    st.success("Resume text extracted successfully")
                else:
                    st.error(f"Could not extract text from {uploaded_file.name}. Skipping.")
                    continue

            # --- Analyze skills ---
            with st.spinner("Analyzing skills..."):
                skills_found = skill_match(resume_text, BANKING_SKILLS, model)
                total_categories = len(skills_found)
                matched_categories = sum(1 for v in skills_found.values() if v)
                job_skills = extract_job_skills(job_description, BANKING_SKILLS)
                missing_skills = get_missing_skills(job_skills, skills_found)
                skill_score = (matched_categories / total_categories) * 100

            # --- Calculate similarity ---
            with st.spinner("Calculating similarity..."):
                result = calculate_similarity(resume_text, job_description)
                match_score = result["similarity"]

            # --- Extract experience ---
            with st.spinner("Extracting experience..."):
                job_exp = extract_experience(job_description)
                resume_exp = extract_experience(resume_text)
                exp_result = calculate_experience_score(resume_exp, job_exp)
                exp_score = exp_result["score"]

            # --- Weighted final score (UPDATED FOR OPTION 2) ---
            weights = {"similarity": 0.6, "skills": 0.3, "experience": 0.1}
            
            # If job has no experience requirement, remove experience from scoring entirely
            if exp_result["status"] in ["no_requirement", "no_data"]:
                # Redistribute experience weight to similarity and skills (60/30 becomes 67/33)
                weights["similarity"] = 0.67
                weights["skills"] = 0.33
                weights["experience"] = 0
                exp_score = 0  # Experience not used

            final_score = (
                match_score * weights["similarity"]
                + skill_score * weights["skills"]
                + exp_score * weights["experience"]
            )

            st.subheader(f"Final Match Score: {final_score:.2f}%")

            # --- Explanation engine ---
            exp_used = (weights["experience"] > 0)
            explanation = generate_explanation(skills_found, missing_skills, match_score, exp_score, exp_used=exp_used)
            
            # Display Strengths if they exist
            if explanation["strengths"]:
                st.markdown("**Strengths:**")
                for s in explanation["strengths"]:
                    st.markdown(s)

            # Display Gaps if they exist
            if explanation["gaps"]:
                st.markdown("**Gaps:**")
                for g in explanation["gaps"]:
                    st.markdown(g)

    elif not uploaded_files:
        st.warning("Please upload at least one resume file.")
    elif not job_description:
        st.warning("Please paste a job description.")
    elif not gender:
        st.warning("Please select your gender")
    elif not age:
        st.warning("Please enter your age")

st.markdown("""
<style>
.stTextArea [data-testid="stExpander"] div:first-child {height: 200px;}
</style>
""", unsafe_allow_html=True)