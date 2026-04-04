
import streamlit as st
from resume_parser import extract_text_from_pdf
from text_preprocessing import preprocess_text
from similarity import calculate_similarity
import os

st.set_page_config(page_title="AI Resume Screening System")

st.title("AI Resume Screening System")
st.markdown("Upload a resume and paste a job description to get a match score.")

# # Job Description Input
st.header("1. Job Description")
job_description = st.text_area("Paste the Job Description here:", height=200)

# # Resume Upload
st.header("2. Upload Resume (PDF)")
# modify this to accept docx, .txt files aswell
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

match_score = None

if st.button("Evaluate Match"):
    if uploaded_file is not None and job_description:
        with st.spinner("Extracting text from resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if resume_text:
                st.success("Resume text extracted successfully!")
            else:
                st.error("Could not extract text from resume. Please try another PDF.")
                st.stop()
                
        with st.spinner("Preprocessing texts..."):
            processed_resume = preprocess_text(resume_text)
            processed_job_description = preprocess_text(job_description)
            print(f"Processed job desc: {processed_job_description}")
            st.success("Texts preprocessed successfully.")
            
            
        with st.spinner("Calculating similarity..."):
            match_score = calculate_similarity(processed_resume, processed_job_description)
            st.success("Similarity calculated.")
            
        if match_score is not None:
            st.header("3. Match Score")
            st.markdown(f"## <span style='color:green;'>Match Score is {match_score:.2f}%</span>", unsafe_allow_html=True)
            
    elif uploaded_file is None:
            st.warning("Please upload a resume PDF.")
    elif not job_description:
        st.warning("Please paste a job description.")
        
    

st.markdown("""
<style>
.stTextArea [data-testid="stExpander"] div:first-child {height: 200px;}
</style>
""", unsafe_allow_html=True) #what does unsafe_allow_html do?

