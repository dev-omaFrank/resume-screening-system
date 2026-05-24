"""Admin Dashboard - Internal Management Interface"""
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime
from utils.email_sender import send_interview_email

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.theme import apply_theme, toggle_theme, LIGHT_THEME, DARK_THEME
from database.db_manager import (
    get_all_vacancies, create_vacancy, update_vacancy, delete_vacancy,
    get_all_submissions, get_submission_by_id, update_submission_status,
    delete_submission, get_vacancy_by_id
)
from utils.text_extractor import extract_text

# Page config
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def render_badge(text, badge_type, theme):
    """Render a status badge."""
    badge_class = f"badge-{badge_type}"
    return f'<span class="badge {badge_class}">{text}</span>'

def render_table_header(headers, theme):
    """Render table header row."""
    cols_html = ""
    for header in headers:
        cols_html += f'<div style="flex: 1; font-weight: 600;">{header}</div>'
    return f'<div class="table-header" style="display: flex;">{cols_html}</div>'

def render_pagination(current_page, total_pages, key_prefix, theme):
    """Render pagination controls."""
    cols = st.columns([1, 3, 1])

    with cols[1]:
        page_cols = st.columns(min(total_pages, 7))
        for i, col in enumerate(page_cols):
            page_num = i + 1
            if page_num <= total_pages:
                with col:
                    if st.button(str(page_num), key=f"{key_prefix}_page_{page_num}", 
                                type="primary" if page_num == current_page else "secondary",
                                use_container_width=True):
                        st.session_state[f"{key_prefix}_current_page"] = page_num
                        st.rerun()

    with cols[0]:
        if current_page > 1:
            if st.button("◀", key=f"{key_prefix}_prev"):
                st.session_state[f"{key_prefix}_current_page"] = current_page - 1
                st.rerun()

    with cols[2]:
        if current_page < total_pages:
            if st.button("▶", key=f"{key_prefix}_next"):
                st.session_state[f"{key_prefix}_current_page"] = current_page + 1
                st.rerun()

def show_vacancy_modal(vacancy_id=None, theme=None):
    """Show create/edit vacancy modal."""
    is_edit = vacancy_id is not None
    vacancy = None

    if is_edit:
        vacancy = get_vacancy_by_id(vacancy_id)

    modal_title = "Edit Vacancy" if is_edit else "Create new Vacancy"

    st.markdown(f"""
    <div style="font-size: 20px; font-weight: 700; color: {theme['text']}; margin-bottom: 20px;">
        {modal_title}
    </div>
    """, unsafe_allow_html=True)

    with st.form("vacancy_form"):
        job_title = st.text_input(
            "Job Title *",
            value=vacancy['job_title'] if vacancy else "",
            placeholder="e.g., Senior Software Engineer"
        )

        job_description = st.text_area(
            "Job Description *",
            value=vacancy['job_description'] if vacancy else "",
            height=150,
            placeholder="Paste job description..."
        )

        ai_gender = st.selectbox(
            "AI Should Favour Which Gender *",
            options=["None", "Male", "Female", "Male and Female"],
            index=["None", "Male", "Female", "Male and Female"].index(vacancy['ai_gender_preference']) if vacancy else 0
        )

        ai_age = st.text_input(
            "AI Should Favour Age",
            value=vacancy['ai_age_preference'] if vacancy else "",
            placeholder="e.g., less than 27, 25-35"
        )

        col1, col2 = st.columns(2)
        with col1:
            ask_dob = st.checkbox(
                "Ask for date of birth during application",
                value=bool(vacancy['ask_for_date_of_birth']) if vacancy else False
            )
        with col2:
            ask_gender = st.checkbox(
                "Ask for gender during application",
                value=bool(vacancy['ask_for_gender']) if vacancy else False
            )

        col_cancel, col_submit = st.columns([1, 1])

        with col_cancel:
            cancel = st.form_submit_button("Cancel", use_container_width=True)

        with col_submit:
            submitted = st.form_submit_button("Create" if not is_edit else "Update", 
                                             type="primary", use_container_width=True)

        if cancel:
            st.session_state.show_vacancy_modal = False
            st.session_state.editing_vacancy = None
            st.rerun()

        if submitted:
            if not job_title.strip():
                st.error("Job Title is required")
            elif not job_description.strip():
                st.error("Job Description is required")
            else:
                if is_edit:
                    update_vacancy(
                        vacancy_id,
                        job_title=job_title.strip(),
                        job_description=job_description.strip(),
                        ai_gender_preference=ai_gender,
                        ai_age_preference=ai_age.strip() if ai_age else None,
                        ask_for_date_of_birth=int(ask_dob),
                        ask_for_gender=int(ask_gender)
                    )
                    st.success("Vacancy updated successfully!")
                else:
                    vid, link = create_vacancy(
                        job_title=job_title.strip(),
                        job_description=job_description.strip(),
                        ai_gender_preference=ai_gender,
                        ai_age_preference=ai_age.strip() if ai_age else None,
                        ask_for_date_of_birth=int(ask_dob),
                        ask_for_gender=int(ask_gender)
                    )
                    st.success(f"Vacancy created! Application link: {link}")

                st.session_state.show_vacancy_modal = False
                st.session_state.editing_vacancy = None
                st.rerun()

def show_vacancy_details(vacancy_id, theme):
    """Show vacancy details modal."""
    vacancy = get_vacancy_by_id(vacancy_id)
    if not vacancy:
        st.error("Vacancy not found")
        return

    st.markdown(f"""
    <div style="font-size: 20px; font-weight: 700; color: {theme['text']}; margin-bottom: 16px;">
        Vacancy Details
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Job Title</div>
            <div style="font-size: 16px; font-weight: 600; color: {theme['text']};">{vacancy['job_title']}</div>
        </div>
        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Job Description</div>
            <div style="font-size: 14px; color: {theme['text']};">{vacancy['job_description']}</div>
        </div>
        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">AI Gender Preference</div>
            <div style="font-size: 14px; color: {theme['text']};">{vacancy['ai_gender_preference']}</div>
        </div>
        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">AI Age Preference</div>
            <div style="font-size: 14px; color: {theme['text']};">{vacancy['ai_age_preference'] or 'None'}</div>
        </div>
        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Application Link</div>
            <div style="font-size: 14px; color: {theme['primary']};">{vacancy['application_link']}</div>
        </div>
        <div>
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Status</div>
            {render_badge(vacancy['status'], 'success' if vacancy['status'] == 'Open' else 'danger', theme)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Close", use_container_width=True):
        st.session_state.show_vacancy_details = False
        st.session_state.viewing_vacancy = None
        st.rerun()

def show_submission_details(submission_id, theme):
    """Show submission details modal."""
    submission = get_submission_by_id(submission_id)
    if not submission:
        st.error("Submission not found")
        return

    st.markdown(f"""
    <div style="font-size: 20px; font-weight: 700; color: {theme['text']}; margin-bottom: 16px;">
        Candidate Details
    </div>
    """, unsafe_allow_html=True)

    # Determine badge type
    score = submission['match_score'] or 0
    if score >= 70:
        badge_type = 'success'
    elif score >= 50:
        badge_type = 'warning'
    else:
        badge_type = 'danger'

    status = "Employable" if score >= 70 else "Fair" if score >= 50 else "Not employable"

    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div style="font-size: 18px; font-weight: 600; color: {theme['text']};">
                {submission['candidate_name']}
            </div>
            {render_badge(status, badge_type, theme)}
        </div>

        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Email</div>
            <div style="font-size: 14px; color: {theme['text']};">{submission['email'] or 'N/A'}</div>
        </div>

        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Vacancy</div>
            <div style="font-size: 14px; color: {theme['text']};">{submission['vacancy_title']}</div>
        </div>

        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Resume Rating</div>
            <div style="font-size: 24px; font-weight: 700; color: {theme['primary']};">{score:.0f}%</div>
        </div>

        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">AI Recommendation</div>
            <div style="font-size: 14px; color: {theme['text']}; line-height: 1.6;">
                {submission['ai_recommendation'] or 'No recommendation available'}
            </div>
        </div>

        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Strengths</div>
            <div style="font-size: 14px; color: {theme['success']};">
                {submission['strengths'] or 'None identified'}
            </div>
        </div>

        <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Gaps</div>
            <div style="font-size: 14px; color: {theme['danger']};">
                {submission['gaps'] or 'None identified'}
            </div>
        </div>

        <div>
            <div style="font-size: 12px; color: {theme['text_secondary']}; margin-bottom: 4px;">Submission Date</div>
            <div style="font-size: 14px; color: {theme['text']};">{submission['submission_date']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resume preview/download
    if submission['resume_file_path'] and os.path.exists(submission['resume_file_path']):
        st.markdown(f"""
        <div style="margin-top: 16px;">
            <div style="font-size: 14px; font-weight: 600; color: {theme['text']}; margin-bottom: 8px;">
                Resume Preview
            </div>
        </div>
        """, unsafe_allow_html=True)

        try:
            resume_text = extract_text(submission['resume_file_path'])
            with st.expander("View Resume Content"):
                st.text_area("", value=resume_text[:2000] + ("..." if len(resume_text) > 2000 else ""), 
                            height=300, disabled=True)
        except:
            st.info("Unable to preview resume content")

        with open(submission['resume_file_path'], 'rb') as f:
            st.download_button(
                "Download Resume",
                f.read(),
                file_name=os.path.basename(submission['resume_file_path']),
                use_container_width=True
            )

    if st.button("Close", use_container_width=True):
        st.session_state.show_submission_details = False
        st.session_state.viewing_submission = None
        st.rerun()

def render_vacancies_tab(theme):
    """Render Job Vacancies tab."""
    st.markdown('<div class="sub-header">Job Vacancies</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color: {theme["text_secondary"]}; margin-bottom: 20px;">Create and manage jobs vacancies</div>', unsafe_allow_html=True)

    # Search and Create button row
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

    with col1:
        search = st.text_input("🔍 Search", placeholder="Search vacancies...", key="vacancy_search")

    with col2:
        if st.button("➕ New Vacancy", use_container_width=True, type="primary"):
            st.session_state.show_vacancy_modal = True
            st.session_state.editing_vacancy = None
            # st.rerun()

    # Vacancy modal
    if st.session_state.get('show_vacancy_modal', False):
        show_vacancy_modal(st.session_state.get('editing_vacancy'), theme)
        return

    # Vacancy details modal
    if st.session_state.get('show_vacancy_details', False):
        show_vacancy_details(st.session_state.get('viewing_vacancy'), theme)
        return

    # Get and filter vacancies
    vacancies = get_all_vacancies()

    if search:
        search_lower = search.lower()
        vacancies = [v for v in vacancies if 
                     search_lower in v['job_title'].lower() or 
                     search_lower in v['job_description'].lower() or
                     search_lower in v['status'].lower()]

    # Pagination
    if 'vacancies_current_page' not in st.session_state:
        st.session_state.vacancies_current_page = 1

    items_per_page = 10
    total_pages = max(1, (len(vacancies) + items_per_page - 1) // items_per_page)
    current_page = st.session_state.vacancies_current_page

    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_vacancies = vacancies[start_idx:end_idx]

    # Table
    if not page_vacancies:
        st.info("No vacancies found")
    else:
        # Header
        header_cols = st.columns([2, 1, 3, 1, 1, 1, 2, 1])
        headers = ["Job Title", "Gender", "Job Description", "Submitted", "Progressed", "Status", "Application Link", "Actions"]
        for col, header in zip(header_cols, headers):
            col.markdown(f"**{header}**")

        st.markdown("---")

        for vacancy in page_vacancies:
            # Status badge
            if vacancy['status'] == 'Open':
                badge_type = 'success'
            elif vacancy['status'] == 'Pending':
                badge_type = 'warning'
            else:
                badge_type = 'danger'

            cols = st.columns([2, 1, 3, 1, 1, 1, 2, 1])

            with cols[0]:
                st.write(vacancy['job_title'])
            with cols[1]:
                st.write(vacancy['ai_gender_preference'])
            with cols[2]:
                desc = vacancy['job_description'][:50] + "..." if len(vacancy['job_description']) > 50 else vacancy['job_description']
                st.write(desc)
            with cols[3]:
                st.write(str(vacancy['submitted_count']))
            with cols[4]:
                st.write(str(vacancy['progressed_count']))
            with cols[5]:
                st.markdown(render_badge(vacancy['status'], badge_type, theme), unsafe_allow_html=True)
            with cols[6]:
                if vacancy['application_link']:
                    if st.button("🔗", key=f"copy_link_{vacancy['id']}", help="Copy application link"):
                        st.code(vacancy['application_link'])
                        st.success("Link copied to clipboard!")
            with cols[7]:
                with st.popover("⋮"):
                    if st.button("View details", key=f"view_vac_{vacancy['id']}"):
                        st.session_state.show_vacancy_details = True
                        st.session_state.viewing_vacancy = vacancy['id']
                        st.rerun()
                    if st.button("Edit", key=f"edit_vac_{vacancy['id']}"):
                        st.session_state.show_vacancy_modal = True
                        st.session_state.editing_vacancy = vacancy['id']
                        st.rerun()
                    if st.button("Copy application link", key=f"copy_vac_{vacancy['id']}"):
                        st.code(vacancy['application_link'])
                    if vacancy['status'] == 'Open':
                        if st.button("Mark as closed", key=f"close_vac_{vacancy['id']}"):
                            update_vacancy(vacancy['id'], status='Closed')
                            st.success("Vacancy marked as closed")
                            st.rerun()
                            
                    if vacancy['status'] == 'Closed':
                        if st.button("Reopen Application", key=f"close_vac_{vacancy['id']}"):
                            update_vacancy(vacancy['id'], status='Open')
                            st.success("Vacancy Re-opened")
                            st.rerun()
                            
                    if st.button("Delete", key=f"del_vac_{vacancy['id']}"):
                        delete_vacancy(vacancy['id'])
                        st.success("Vacancy deleted")
                        st.rerun()

            st.markdown("---")

    # Pagination
    if total_pages > 1:
        render_pagination(current_page, total_pages, "vacancies", theme)

    st.write(f"Page {current_page} of {total_pages}")

def render_submitted_resumes_tab(theme):
    """Render Submitted Resumes tab."""
    st.markdown('<div class="sub-header" style="colour:gray;">Submitted Resumes</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color: {theme["text_secondary"]}; margin-bottom: 20px;">Review and screen submitted applications</div>', unsafe_allow_html=True)

    # Search and filter row
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search submissions...", key="submission_search")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Employable", "Fair", "Not employable"], key="sub_status_filter")

    # Get submissions
    submissions = get_all_submissions(status='submitted')

    # Apply filters
    if search:
        search_lower = search.lower()
        submissions = [s for s in submissions if 
                       search_lower in s['candidate_name'].lower() or 
                       search_lower in (s['email'] or '').lower() or
                       search_lower in (s['vacancy_title'] or '').lower()]

    if status_filter != "All":
        # Current code - status_filter isn't being checked properly
        submissions = [s for s in submissions if 
                    (status_filter == "Employable" and s['match_score'] >= 70) or
                    (status_filter == "Fair" and 50 <= s['match_score'] < 70) or
                    (status_filter == "Not employable" and s['match_score'] < 50)]

    # Pagination
    if 'submitted_current_page' not in st.session_state:
        st.session_state.submitted_current_page = 1

    items_per_page = 10
    total_pages = max(1, (len(submissions) + items_per_page - 1) // items_per_page)
    current_page = st.session_state.submitted_current_page

    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_submissions = submissions[start_idx:end_idx]

    # Submission details modal
    if st.session_state.get('show_submission_details', False):
        show_submission_details(st.session_state.get('viewing_submission'), theme)
        return

    # Table
    if not page_submissions:
        st.info("No submitted resumes found")
    else:
        header_cols = st.columns([2, 2, 2, 3, 1, 1, 1, 1])
        headers = ["Name", "Email", "Vacancy", "AI Recommendation", "Rating", "Status", "View", "Actions"]
        for col, header in zip(header_cols, headers):
            col.markdown(f"**{header}**")

        st.markdown("---")

        for sub in page_submissions:
            score = sub['match_score'] or 0

            if score >= 70:
                badge_type = 'success'
                status_text = "Employable"
            elif score >= 40:
                badge_type = 'warning'
                status_text = "Fair"
            else:
                badge_type = None
                status_text = None
            cols = st.columns([2, 2, 2, 3, 1, 1, 1, 1])

            with cols[0]:
                st.write(sub['candidate_name'])
            with cols[1]:
                st.write(sub['email'] or 'N/A')
            with cols[2]:
                st.write(sub['vacancy_title'] or 'N/A')
            with cols[3]:
                rec = (sub['ai_recommendation'] or '')[:40] + "..." if len(sub['ai_recommendation'] or '') > 40 else (sub['ai_recommendation'] or 'N/A')
                st.write(rec)
            with cols[4]:
                st.write(f"{score:.0f}%")
            with cols[5]:
                if badge_type and status_text:
                    st.markdown(render_badge(status_text, badge_type, theme), unsafe_allow_html=True)
            with cols[6]:
                if st.button("👁", key=f"view_sub_{sub['id']}", help="View resume"):
                    st.session_state.show_submission_details = True
                    st.session_state.viewing_submission = sub['id']
                    st.rerun()
            with cols[7]:
                with st.popover("⋮"):
                    if st.button("View Details", key=f"details_sub_{sub['id']}"):
                        st.session_state.show_submission_details = True
                        st.session_state.viewing_submission = sub['id']
                        st.rerun()
                    if st.button("Move to Progressed", key=f"progress_sub_{sub['id']}"):
                        update_submission_status(sub['id'], 'progressed')
                        st.success("Moved to Progressed Resumes")
                        st.rerun()
                    if st.button("Delete", key=f"del_sub_{sub['id']}"):
                        delete_submission(sub['id'])
                        st.success("Submission deleted")
                        st.rerun()

            st.markdown("---")

    # Pagination
    if total_pages > 1:
        render_pagination(current_page, total_pages, "submitted", theme)

    st.write(f"Page {current_page} of {total_pages}")

def render_progressed_resumes_tab(theme):
    """Render Progressed Resumes tab."""
    st.markdown('<div class="sub-header">Progressed Resumes</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color: {theme["text_secondary"]}; margin-bottom: 20px;">Candidates in interview phase</div>', unsafe_allow_html=True)

    # Search and filter row
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search progressed candidates...", key="progressed_search")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Employable", "Fair", "Not employable"], key="prog_status_filter")

    # Get progressed submissions
    submissions = get_all_submissions(status='progressed')

    # Apply filters
    if search:
        search_lower = search.lower()
        submissions = [s for s in submissions if 
                       search_lower in s['candidate_name'].lower() or 
                       search_lower in (s['email'] or '').lower() or
                       search_lower in (s['vacancy_title'] or '').lower()]

    if status_filter != "All":
        # Option 1: Simple fix with 40 threshold
        submissions = [s for s in submissions if 
                    (status_filter == "All") or
                    (status_filter == "Employable" and (s['match_score'] or 0) >= 70) or
                    (status_filter == "Fair" and 40 <= (s['match_score'] or 0) < 70)]

    # Pagination
    if 'progressed_current_page' not in st.session_state:
        st.session_state.progressed_current_page = 1

    items_per_page = 10
    total_pages = max(1, (len(submissions) + items_per_page - 1) // items_per_page)
    current_page = st.session_state.progressed_current_page

    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_submissions = submissions[start_idx:end_idx]

    # Submission details modal
    if st.session_state.get('show_progressed_details', False):
        show_submission_details(st.session_state.get('viewing_progressed'), theme)
        return

    # Table
    if not page_submissions:
        st.info("No progressed resumes found")
    else:
        header_cols = st.columns([2, 2, 2, 3, 1, 1, 1, 1])
        headers = ["Name", "Email", "Vacancy", "AI Recommendation", "Rating", "Status", "View", "Actions"]
        for col, header in zip(header_cols, headers):
            col.markdown(f"**{header}**")

        st.markdown("---")

        for sub in page_submissions:
            score = sub['match_score'] or 0

            if score >= 70:
                badge_type = 'success'
                status_text = "Employable"
            elif score >= 40:
                badge_type = 'warning'
                status_text = "Fair"
            else:
                badge_type = None
                status_text = None

            cols = st.columns([2, 2, 2, 3, 1, 1, 1, 1])

            with cols[0]:
                st.write(sub['candidate_name'])
            with cols[1]:
                st.write(sub['email'] or 'N/A')
            with cols[2]:
                st.write(sub['vacancy_title'] or 'N/A')
            with cols[3]:
                rec = (sub['ai_recommendation'] or '')[:40] + "..." if len(sub['ai_recommendation'] or '') > 40 else (sub['ai_recommendation'] or 'N/A')
                st.write(rec)
            with cols[4]:
                st.write(f"{score:.0f}%")
            with cols[5]:
                st.markdown(render_badge(status_text, badge_type, theme), unsafe_allow_html=True)
            with cols[6]:
                if st.button("👁", key=f"view_prog_{sub['id']}", help="View resume"):
                    st.session_state.show_progressed_details = True
                    st.session_state.viewing_progressed = sub['id']
                    st.rerun()
            with cols[7]:
                with st.popover("⋮"):
                    if st.button("View Details", key=f"details_prog_{sub['id']}"):
                        st.session_state.show_progressed_details = True
                        st.session_state.viewing_progressed = sub['id']
                        st.rerun()
                        
                    if st.button("Send Interview Email", key=f"email_sub_{sub['id']}"):
                        email_sent = send_interview_email(
                            to_email = sub['email'],
                            candidate_name = sub['candidate_name'],
                            vacancy_title = sub['vacancy_title']
                        )
                        if email_sent:
                            update_submission_status(sub['id'], 'progressed')
                            st.success("Interview Email sent")
                        else:
                            st.error("❌ Failed to send email")
                            
                        exit
                    
                    if st.button("Move Back to Submitted", key=f"back_prog_{sub['id']}"):
                        update_submission_status(sub['id'], 'submitted')
                        st.success("Moved back to Submitted Resumes")
                        st.rerun()
                    if st.button("Delete", key=f"del_prog_{sub['id']}"):
                        delete_submission(sub['id'])
                        st.success("Submission deleted")
                        st.rerun()

            st.markdown("---")

    # Pagination
    if total_pages > 1:
        render_pagination(current_page, total_pages, "progressed", theme)

    st.write(f"Page {current_page} of {total_pages}")

def main():
    """Main admin dashboard."""
    # Apply theme
    theme = apply_theme()

    # Theme toggle
    col1, col2 = st.columns([0.9, 0.1])
    with col2:
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        if st.button(theme_icon, key="admin_theme_toggle", help="Toggle theme"):
            toggle_theme()

    with col1:
        st.markdown('<div class="main-header">Admin Dashboard</div>', unsafe_allow_html=True)

    # Initialize session state for modals
    if 'show_vacancy_modal' not in st.session_state:
        st.session_state.show_vacancy_modal = False
    if 'editing_vacancy' not in st.session_state:
        st.session_state.editing_vacancy = None
    if 'show_vacancy_details' not in st.session_state:
        st.session_state.show_vacancy_details = False
    if 'viewing_vacancy' not in st.session_state:
        st.session_state.viewing_vacancy = None
    if 'show_submission_details' not in st.session_state:
        st.session_state.show_submission_details = False
    if 'viewing_submission' not in st.session_state:
        st.session_state.viewing_submission = None
    if 'show_progressed_details' not in st.session_state:
        st.session_state.show_progressed_details = False
    if 'viewing_progressed' not in st.session_state:
        st.session_state.viewing_progressed = None
        
    # Inject CSS to change tab label text color to gray
    st.markdown("""
    <style>
        .stTabs button[role="tab"] p {
            color: gray !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Job Vacancies", "Submitted Resumes", "Progressed Resumes"])

    with tab1:
        render_vacancies_tab(theme)

    with tab2:
        render_submitted_resumes_tab(theme)

    with tab3:
        render_progressed_resumes_tab(theme)

if __name__ == "__main__":
    main()
