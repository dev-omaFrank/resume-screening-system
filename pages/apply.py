"""User Screening Page - Public-facing application form"""
import streamlit as st
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.theme import apply_theme, LIGHT_THEME, DARK_THEME
from database.db_manager import get_vacancy_by_id, create_submission
from utils.text_extractor import extract_text
from core.similarity import calculate_similarity, preprocess_for_tfidf
from core.skills import extract_skills, match_skills
from core.experience import extract_years_of_experience, score_experience
from core.explanation import generate_explanation, get_status, combine_scores

def main():
    """Main application page for candidates."""
    # Apply theme
    theme = apply_theme()

    # Get vacancy_id from URL query parameter
    query_params = st.query_params
    vacancy_id = query_params.get("vacancy_id", None)

    # Header
    st.markdown('<div class="main-header">AI-Based Resume Screening System</div>', unsafe_allow_html=True)

    # Handle missing vacancy_id
    if not vacancy_id:
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 40px;">
            <div style="font-size: 48px; margin-bottom: 16px;">🔗</div>
            <div style="font-size: 18px; font-weight: 600; color: {theme['text']}; margin-bottom: 8px;">
                Invalid Application Link
            </div>
            <div style="color: {theme['text_secondary']}; font-size: 14px;">
                Please use the application link provided by the employer.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    try:
        vacancy_id = int(vacancy_id)
    except (ValueError, TypeError):
        st.error("Invalid vacancy ID")
        return

    # Fetch vacancy details
    vacancy = get_vacancy_by_id(vacancy_id)

    if not vacancy:
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 40px;">
            <div style="font-size: 48px; margin-bottom: 16px;">❌</div>
            <div style="font-size: 18px; font-weight: 600; color: {theme['text']}; margin-bottom: 8px;">
                Vacancy Not Found
            </div>
            <div style="color: {theme['text_secondary']}; font-size: 14px;">
                The position you are looking for does not exist or has been removed.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Check if vacancy is closed
    if vacancy['status'] == 'Closed':
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 40px;">
            <div style="font-size: 48px; margin-bottom: 16px;">🔒</div>
            <div style="font-size: 18px; font-weight: 600; color: {theme['text']}; margin-bottom: 8px;">
                Position Closed
            </div>
            <div style="color: {theme['text_secondary']}; font-size: 14px;">
                This position is no longer accepting applications.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Display vacancy info
    st.markdown(f'<div class="sub-header">{vacancy["job_title"]}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div style="font-size: 14px; font-weight: 600; color: {theme['text']}; margin-bottom: 8px;">
            Job Description
        </div>
        <div style="color: {theme['text_secondary']}; font-size: 14px; line-height: 1.6;">
            {vacancy['job_description']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Application Form
    st.markdown(f'<div class="section-title" style="margin-top: 24px;">Submit Your Application</div>', unsafe_allow_html=True)

    with st.form("application_form", clear_on_submit=True):
        st.markdown("""
        <style>
            /* Something here might be hiding labels */
            .stTextInput label {
                display: block !important;
                color: gray;
            }
        </style>
        """, unsafe_allow_html=True)
        # Name Field
        name = st.text_input(
            "Full Name *",
            placeholder="Your full name",
            help="Enter your full name as it appears on your resume"
        )

        # Email Field
        email = st.text_input(
            "Email Address *",
            placeholder="your.email@example.com",
            help="Enter a valid email address"
        )

        # Date of Birth (conditional)
        date_of_birth = None
        if vacancy['ask_for_date_of_birth']:
            date_of_birth = st.date_input(
                "Date of Birth *",
                help="Select your date of birth"
            )

        # Gender (conditional)
        gender = None
        if vacancy['ask_for_gender']:
            gender = st.selectbox(
                "Gender *",
                options=["Enter your gender", "Male", "Female"],
                placeholder="Enter Gender",
                help="Select your gender"
            )

        # Resume Upload
        st.markdown(f"""
        <div style="margin-bottom: 8px;">
            <span style="font-size: 14px; font-weight: 500; color: {theme['text']};">Resume Upload *</span>
        </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload your resume (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="You can upload multiple files if needed"
        )

        # Submit Button
        submitted = st.form_submit_button(
            "Submit Application",
            use_container_width=True,
            type="primary"
        )

        if submitted:
            # Validation
            errors = []
            if not name or not name.strip():
                errors.append("Full Name is required")
            if not email or not email.strip():
                errors.append("Email Address is required")
            elif "@" not in email:
                errors.append("Please enter a valid email address")
            if vacancy['ask_for_date_of_birth'] and not date_of_birth:
                errors.append("Date of Birth is required")
            if vacancy['ask_for_gender'] and not gender or gender == "Enter your gender":
                errors.append("Gender is required")
            if not uploaded_files:
                errors.append("Please upload at least one resume file")

            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Process submission
                try:
                    # Save resume files
                    resume_paths = []
                    for uploaded_file in uploaded_files:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        file_ext = uploaded_file.name.split('.')[-1]
                        file_name = f"{vacancy_id}_{name.replace(' ', '_')}_{timestamp}.{file_ext}"
                        file_path = os.path.join('data', 'resumes', file_name)

                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, 'wb') as f:
                            f.write(uploaded_file.getvalue())

                        resume_paths.append(file_path)

                    # Extract text and calculate scores (for admin review, NOT shown to user)
                    resume_text = ""
                    for path in resume_paths:
                        text = extract_text(path)
                        resume_text += text + " "
                        
                    # preprocess the text
                    resume_text = preprocess_for_tfidf(resume_text)
                    job_description = preprocess_for_tfidf(vacancy['job_description'])

                    ### Calculate similarity
                    match_score = calculate_similarity(resume_text, job_description)

                    # Extract skills
                    resume_skills = extract_skills(resume_text)
                    job_skills = extract_skills(job_description)
                    skills_match = match_skills(resume_skills, job_skills)

                    # Experience
                    years = extract_years_of_experience(resume_text)
                    exp_score = score_experience(years)
                    
                    # Combine all scores
                    final_score = combine_scores(
                        match_score,
                        skills_match['match_percentage'],
                        exp_score
                    )

                    # ADD THIS CHECK - Don't save if score is too low
                    if final_score < 20:
                        st.warning("Your resume does not meet the minimum requirements for this position. Thank you for your interest.")
                        st.stop()  
                    
                    # Generate recommendation
                    ai_recommendation = generate_explanation(final_score, skills_match, exp_score)
                    status = get_status(final_score)

                    # Save to database
                    dob_str = date_of_birth.isoformat() if date_of_birth else None

                    create_submission(
                        vacancy_id=vacancy_id,
                        candidate_name=name.strip(),
                        email=email.strip(),
                        date_of_birth=dob_str,
                        gender=gender,
                        resume_file_path=resume_paths[0] if resume_paths else None,
                        match_score=final_score,
                        ai_recommendation=ai_recommendation,
                        strengths=", ".join(skills_match['matched'][:5]),
                        gaps=", ".join(skills_match['missing'][:5])
                    )
                    ###
                    
                    # Success message
                    st.success("✅ Your resume has been submitted successfully. We will review it and get back to you soon.")
                    st.balloons()

                except Exception as e:
                    st.error(f"❌ Failed to process resume. Please ensure the file is valid and try again.")
                    st.exception(e)

if __name__ == "__main__":
    main()
