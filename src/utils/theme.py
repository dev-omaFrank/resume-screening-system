"""Theme and Styling Utilities for AI Resume Screening System"""

# Light Mode Colors
LIGHT_THEME = {
    "primary": "#1D2951",
    "primary_hover": "#2a3a6a",
    "background": "#f8f9fa",
    "surface": "#ffffff",
    "text": "#1a1a1a",
    "text_secondary": "#666666",
    "border": "#e0e0e0",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "success_light": "#d1fae5",
    "warning_light": "#fef3c7",
    "danger_light": "#fee2e2",
}

# Dark Mode Colors
DARK_THEME = {
    "primary": "#3b4a8f",
    "primary_hover": "#4a5fa8",
    "background": "#0f1419",
    "surface": "#1a1f2e",
    "text": "#e8eaed",
    "text_secondary": "#9ca3af",
    "border": "#2d3748",
    "success": "#34d399",
    "warning": "#fbbf24",
    "danger": "#f87171",
    "success_light": "#064e3b",
    "warning_light": "#78350f",
    "danger_light": "#7f1d1d",
}

def get_css(theme):
    """Generate CSS based on theme."""
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    .stApp {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
    }}

    .main-header {{
        font-size: 24px;
        font-weight: 700;
        color: {theme['text']};
        margin-bottom: 8px;
    }}

    .sub-header {{
        font-size: 20px;
        font-weight: 700;
        color: {theme['text']};
        margin-bottom: 16px;
    }}

    .section-title {{
        font-size: 18px;
        font-weight: 600;
        color: {theme['text']};
        margin-bottom: 12px;
    }}

    .card {{
        background-color: {theme['surface']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .badge-success {{
        background-color: {theme['success_light']};
        color: {theme['success']};
    }}

    .badge-warning {{
        background-color: {theme['warning_light']};
        color: {theme['warning']};
    }}

    .badge-danger {{
        background-color: {theme['danger_light']};
        color: {theme['danger']};
    }}

    .btn-primary {{
        background-color: {theme['primary']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }}

    .btn-primary:hover {{
        background-color: {theme['primary_hover']};
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}

    .btn-outline {{
        background-color: transparent;
        color: {theme['text']};
        border: 1px solid {theme['border']};
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
        cursor: pointer;
    }}

    .search-input {{
        background-color: {theme['surface']};
        border: 1px solid {theme['border']};
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 14px;
        color: {theme['text']};
        width: 100%;
    }}

    .search-input:focus {{
        outline: none;
        border-color: {theme['primary']};
        box-shadow: 0 0 0 3px rgba(29, 41, 81, 0.1);
    }}

    .table-container {{
        background-color: {theme['surface']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        overflow: hidden;
    }}

    .table-header {{
        background-color: {theme['background']};
        padding: 12px 16px;
        font-weight: 600;
        font-size: 14px;
        color: {theme['text']};
        border-bottom: 1px solid {theme['border']};
    }}

    .table-row {{
        padding: 12px 16px;
        border-bottom: 1px solid {theme['border']};
        font-size: 14px;
        color: {theme['text']};
        display: flex;
        align-items: center;
    }}

    .table-row:hover {{
        background-color: {theme['background']};
    }}

    .action-btn {{
        background: none;
        border: none;
        color: {theme['text_secondary']};
        cursor: pointer;
        padding: 6px;
        border-radius: 4px;
        transition: all 0.2s;
    }}

    .action-btn:hover {{
        background-color: {theme['background']};
        color: {theme['text']};
    }}

    .pagination {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 16px;
    }}

    .page-btn {{
        padding: 6px 12px;
        border: 1px solid {theme['border']};
        background-color: {theme['surface']};
        color: {theme['text']};
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
    }}

    .page-btn.active {{
        background-color: {theme['primary']};
        color: white;
        border-color: {theme['primary']};
    }}

    .modal-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }}

    .modal-content {{
        background-color: {theme['surface']};
        border-radius: 12px;
        padding: 24px;
        max-width: 600px;
        width: 90%;
        max-height: 90vh;
        overflow-y: auto;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }}

    .form-group {{
        margin-bottom: 16px;
    }}

    .form-label {{
        display: block;
        font-size: 14px;
        font-weight: 500;
        color: {theme['text']};
        margin-bottom: 6px;
    }}

    .form-input {{
        width: 100%;
        padding: 10px 14px;
        border: 1px solid {theme['border']};
        border-radius: 6px;
        font-size: 14px;
        color: {theme['text']};
        background-color: {theme['surface']};
    }}

    .form-input:focus {{
        outline: none;
        border-color: {theme['primary']};
        box-shadow: 0 0 0 3px rgba(29, 41, 81, 0.1);
    }}

    .checkbox-group {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
    }}

    .theme-toggle {{
        position: fixed;
        top: 16px;
        right: 16px;
        z-index: 100;
        background-color: {theme['surface']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        padding: 8px 12px;
        cursor: pointer;
        font-size: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}

    @media (max-width: 768px) {{
        .main-header {{ font-size: 20px; }}
        .sub-header {{ font-size: 18px; }}
        .table-row {{ flex-direction: column; align-items: flex-start; }}
        .modal-content {{ width: 95%; padding: 16px; }}
    }}
    </style>
    """

def apply_theme():
    """Apply theme to Streamlit app."""
    import streamlit as st

    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'

    theme = DARK_THEME if st.session_state.theme == 'dark' else LIGHT_THEME

    st.markdown(get_css(theme), unsafe_allow_html=True)

    return theme

def toggle_theme():
    """Toggle between light and dark themes."""
    import streamlit as st

    if st.session_state.theme == 'dark':
        st.session_state.theme = 'light'
    else:
        st.session_state.theme = 'dark'

    st.rerun()
