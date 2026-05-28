import sqlite3
import os
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'submissions.db')

st.set_page_config(page_title="DB Fix", page_icon="🔧")

st.title("🔧 Database Fix")

st.write("Click the button below to add missing columns to the vacancies table.")

if st.button("Run DB Fix"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    errors = []
    successes = []
    
    # Add hiring_company column
    try:
        cursor.execute("ALTER TABLE vacancies ADD COLUMN hiring_company TEXT NOT NULL DEFAULT ''")
        conn.commit()
        successes.append("hiring_company column added")
    except Exception as e:
        errors.append(f"hiring_company: {e}")
    
    conn.close()
    
    if successes:
        for s in successes:
            st.success(f"✅ {s}")
    if errors:
        for e in errors:
            st.error(f"❌ {e}")
    else:
        st.info("All done! You can delete this file now.")