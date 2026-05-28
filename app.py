"""AI-Based Resume Screening System - Main Application"""
import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.theme import apply_theme, toggle_theme, LIGHT_THEME, DARK_THEME
from database.db_manager import get_all_vacancies

def main():
    """Main application entry point."""
    # Apply theme
    theme = apply_theme()

    # Theme toggle button
    col1, col2 = st.columns([0.9, 0.1])
    with col2:
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        if st.button(theme_icon, key="theme_toggle", help="Toggle theme"):
            toggle_theme()

    with col1:
        st.markdown('<div class="main-header">AI-Based Resume Screening System</div>', unsafe_allow_html=True)
        st.markdown('<div style="color: ' + theme['text_secondary'] + '; margin-bottom: 24px;">Welcome to the resume screening platform</div>', unsafe_allow_html=True)

    # Navigation cards
    st.markdown('<div class="sub-header">Get Started</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="card" style="cursor: pointer;">
            <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px; color: {theme['text']};">
                📝 Submit Application
            </div>
            <div style="color: {theme['text_secondary']}; font-size: 14px;">
                Apply for a job vacancy using a provided application link.
            </div>
        </div>
        
        """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="card" style="cursor: pointer;">
                    <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px; color: {theme['text']};">
                        ⁉️ How It Works
                    </div>
                    <div style="color: {theme['text_secondary']}; font-size: 14px;">
                        Use the application link provided by the employer to submit your resume.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Available vacancies preview
    st.markdown('<div class="sub-header" style="margin-top: 32px;">Available Vacancies</div>', unsafe_allow_html=True)

    vacancies = get_all_vacancies()
    open_vacancies = [v for v in vacancies if v['status'] == 'Open']

    if not open_vacancies:
        st.markdown(f"""
        <div class="card" style="text-align: center; padding: 40px;">
            <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
            <div style="font-size: 16px; font-weight: 600; color: {theme['text']}; margin-bottom: 8px;">
                No Open Vacancies
            </div>
            <div style="color: {theme['text_secondary']}; font-size: 14px;">
                There are currently no open positions. Check back later!
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for vacancy in open_vacancies[:5]:  # Show top 5
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 16px; font-weight: 600; color: {theme['text']}; margin-bottom: 4px;">
                                {vacancy['job_title']} posted by {vacancy['hiring_company']}
                            </div>
                            <div style="color: {theme['text_secondary']}; font-size: 13px; margin-bottom: 8px;">
                                {vacancy['job_description'][:30]}{'...' if len(vacancy['job_description']) > 100 else ''}
                            </div>
                            <div style="display: flex; gap: 8px; align-items: center;">
                                <span class="badge badge-success">Open</span>
                                <span style="color: {theme['text_secondary']}; font-size: 12px;">
                                    {vacancy['submitted_count']} applications
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
