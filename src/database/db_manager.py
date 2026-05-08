"""Database Manager for AI Resume Screening System"""
import sqlite3
import os
from datetime import datetime
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'submissions.db')

def get_connection():
    """Get database connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Vacancies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            job_description TEXT NOT NULL,
            ai_gender_preference TEXT DEFAULT 'None',
            ai_age_preference TEXT,
            ask_for_date_of_birth INTEGER DEFAULT 0,
            ask_for_gender INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Open',
            application_link TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Submissions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vacancy_id INTEGER NOT NULL,
            candidate_name TEXT NOT NULL,
            email TEXT,
            date_of_birth DATE,
            gender TEXT,
            resume_file_path TEXT,
            match_score REAL DEFAULT 0,
            ai_recommendation TEXT,
            strengths TEXT,
            gaps TEXT,
            status TEXT DEFAULT 'submitted',
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully")

# ==================== VACANCY METHODS ====================

def create_vacancy(job_title, job_description, ai_gender_preference='None', 
                   ai_age_preference=None, ask_for_date_of_birth=0, ask_for_gender=0):
    """Create a new vacancy and generate application link."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vacancies (job_title, job_description, ai_gender_preference, 
                              ai_age_preference, ask_for_date_of_birth, ask_for_gender, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Open')
    """, (job_title, job_description, ai_gender_preference, ai_age_preference, 
          ask_for_date_of_birth, ask_for_gender))

    vacancy_id = cursor.lastrowid

    # Generate application link
    application_link = f"http://{st.context.url}/apply?vacancy_id={vacancy_id}"

    cursor.execute("""
        UPDATE vacancies SET application_link = ? WHERE id = ?
    """, (application_link, vacancy_id))

    conn.commit()
    conn.close()

    return vacancy_id, application_link

def get_all_vacancies():
    """Get all vacancies with submission counts."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.*,
               (SELECT COUNT(*) FROM submissions WHERE vacancy_id = v.id) as submitted_count,
               (SELECT COUNT(*) FROM submissions WHERE vacancy_id = v.id AND status = 'progressed') as progressed_count
        FROM vacancies v
        ORDER BY v.created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_vacancy_by_id(vacancy_id):
    """Get vacancy by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vacancies WHERE id = ?", (vacancy_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None

def update_vacancy(vacancy_id, **kwargs):
    """Update vacancy fields."""
    conn = get_connection()
    cursor = conn.cursor()

    allowed_fields = ['job_title', 'job_description', 'ai_gender_preference', 
                      'ai_age_preference', 'ask_for_date_of_birth', 'ask_for_gender', 'status']

    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    updates['updated_at'] = datetime.now().isoformat()

    if updates:
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [vacancy_id]

        cursor.execute(f"UPDATE vacancies SET {set_clause} WHERE id = ?", values)
        conn.commit()

    conn.close()
    return True

def delete_vacancy(vacancy_id):
    """Delete vacancy and cascade to submissions."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM vacancies WHERE id = ?", (vacancy_id,))
    conn.commit()
    conn.close()

    return True

# ==================== SUBMISSION METHODS ====================

def create_submission(vacancy_id, candidate_name, email=None, date_of_birth=None,
                      gender=None, resume_file_path=None, match_score=0,
                      ai_recommendation=None, strengths=None, gaps=None):
    """Create a new submission."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO submissions (vacancy_id, candidate_name, email, date_of_birth, 
                                gender, resume_file_path, match_score, ai_recommendation,
                                strengths, gaps, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'submitted')
    """, (vacancy_id, candidate_name, email, date_of_birth, gender, 
          resume_file_path, match_score, ai_recommendation, strengths, gaps))

    submission_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return submission_id

def get_submissions_by_vacancy(vacancy_id, status=None):
    """Get submissions for a vacancy, optionally filtered by status."""
    conn = get_connection()
    cursor = conn.cursor()

    if status:
        cursor.execute("""
            SELECT s.*, v.job_title as vacancy_title
            FROM submissions s
            JOIN vacancies v ON s.vacancy_id = v.id
            WHERE s.vacancy_id = ? AND s.status = ?
            ORDER BY s.submission_date DESC
        """, (vacancy_id, status))
    else:
        cursor.execute("""
            SELECT s.*, v.job_title as vacancy_title
            FROM submissions s
            JOIN vacancies v ON s.vacancy_id = v.id
            WHERE s.vacancy_id = ?
            ORDER BY s.submission_date DESC
        """, (vacancy_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_all_submissions(status=None):
    """Get all submissions, optionally filtered by status."""
    conn = get_connection()
    cursor = conn.cursor()

    if status:
        cursor.execute("""
            SELECT s.*, v.job_title as vacancy_title
            FROM submissions s
            JOIN vacancies v ON s.vacancy_id = v.id
            WHERE s.status = ?
            ORDER BY s.submission_date DESC
        """, (status,))
    else:
        cursor.execute("""
            SELECT s.*, v.job_title as vacancy_title
            FROM submissions s
            JOIN vacancies v ON s.vacancy_id = v.id
            ORDER BY s.submission_date DESC
        """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_submission_by_id(submission_id):
    """Get submission by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.*, v.job_title as vacancy_title, v.job_description
        FROM submissions s
        JOIN vacancies v ON s.vacancy_id = v.id
        WHERE s.id = ?
    """, (submission_id,))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None

def update_submission_status(submission_id, status):
    """Update submission status (submitted/progressed)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE submissions SET status = ? WHERE id = ?
    """, (status, submission_id))

    conn.commit()
    conn.close()

    return True

def delete_submission(submission_id):
    """Delete submission."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM submissions WHERE id = ?", (submission_id,))
    conn.commit()
    conn.close()

    return True

# Initialize database on module import
init_database()
