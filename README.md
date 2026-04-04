# AI Resume Screening System (Week 1 MVP)

## 1. Project Overview
This project implements a basic AI-powered Resume Screening System, focusing on core functionalities for a Week 1 Minimum Viable Product (MVP). The system allows users to upload a PDF resume and paste a job description, then calculates a match score using TF-IDF and cosine similarity. The interface is built with Streamlit, providing an intuitive user experience.

## 2. Features Implemented (Week 1 Scope)
- **PDF Text Extraction**: Extracts raw text content from uploaded PDF resumes.
- **Text Preprocessing**: Cleans and normalizes both resume and job description text by lowercasing, removing punctuation, numbers, special characters, and extra whitespace.
- **Job Description Input**: Accepts job descriptions as free-form text input.
- **TF-IDF + Cosine Similarity**: Utilizes `scikit-learn` to convert text into TF-IDF vectors and computes the cosine similarity between the resume and job description, outputting a percentage match score.
- **Streamlit User Interface**: Provides a simple web interface for uploading resumes, inputting job descriptions, and displaying the match score.

## 3. File-by-File Explanation

### `app.py`
- **Purpose**: The main Streamlit application file. It orchestrates the UI, handles user input (resume upload, job description), calls functions from other modules for text processing and similarity calculation, and displays the final match score.
- **Key Functions**:
  - `st.title`, `st.header`, `st.text_area`, `st.file_uploader`, `st.button`: Streamlit components for UI.
  - Calls `extract_text_from_pdf` from `resume_parser.py`.
  - Calls `preprocess_text` from `text_preprocessing.py`.
  - Calls `calculate_similarity` from `similarity.py`.

### `resume_parser.py`
- **Purpose**: Handles the extraction of text content from PDF files.
- **Key Functions**:
  - `extract_text_from_pdf(pdf_file)`: Takes a file-like object (PDF) as input, uses `pdfplumber` to extract text page by page, and returns the concatenated text. Includes basic error handling for PDF processing.

### `text_preprocessing.py`
- **Purpose**: Contains functions for cleaning and preprocessing raw text data.
- **Key Functions**:
  - `preprocess_text(text)`: Takes a string as input and performs the following operations:
    - Converts text to lowercase.
    - Removes punctuation.
    - Removes numbers.
    - Removes special characters (keeping only letters and spaces).
    - Removes extra whitespace and strips leading/trailing spaces.

### `similarity.py`
- **Purpose**: Implements the logic for calculating text similarity between two documents.
- **Key Functions**:
  - `calculate_similarity(resume_text, job_description_text)`: Takes two preprocessed text strings, initializes a `TfidfVectorizer` from `scikit-learn`, transforms the texts into TF-IDF vectors, computes cosine similarity, and returns the result as a percentage.

### `utils.py` (Optional Helper Functions)
- *Not implemented in this MVP, as current functionality is covered by other modules. This file would typically contain general utility functions not specific to any single module.* 

### `requirements.txt`
- **Purpose**: Lists all Python dependencies required to run the project, along with their version specifications to ensure compatibility and reproducibility.

### `README.md`
- **Purpose**: Provides a comprehensive guide to the project, including its overview, features, file explanations, installation instructions, usage, limitations, and future improvements.

## 4. Installation Instructions

To set up and run this project locally, follow these steps:

1.  **Clone the repository** (if applicable, otherwise download the project folder):
    ```bash
    git clone <repository_url>
    cd resume-screening-system
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    -   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    -   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 5. How to Run the App

Once the dependencies are installed and your virtual environment is active, run the Streamlit application:

```bash
streamlit run app.py
```

This command will open the application in your default web browser.

## 6. Example Usage

1.  Open the Streamlit app in your browser.
2.  In the "Job Description" text area, paste the job description you want to screen against.
3.  Click "Choose a PDF file" under "Upload Resume (PDF)" and select a resume PDF from your local machine.
4.  Click the "Evaluate Match" button.
5.  The "Match Score" will be displayed, indicating the percentage similarity between the resume and the job description.

## 7. Project Limitations (MVP)

As a Week 1 MVP, this system has the following limitations:
-   **Basic Text Matching**: Relies solely on TF-IDF and cosine similarity, which is a statistical method and may not capture semantic nuances or context as effectively as more advanced NLP models.
-   **No Ranking**: Currently, it processes one resume at a time and provides a single match score. It does not rank multiple resumes.
-   **Limited Error Handling**: While basic error handling for PDF extraction is present, robust error handling for all edge cases (e.g., corrupted PDFs, extremely large files) is not fully implemented.
-   **No Bias Reduction**: The system does not include any mechanisms for bias detection or reduction, which is crucial for real-world resume screening.
-   **No Advanced NLP**: Avoids heavy ML models and advanced NLP techniques to keep the MVP lightweight and focused on core functionality.

## 8. Future Improvements (Brief Mention of Week 2 Features)

Future iterations could include:
-   **Resume Ranking**: Implement functionality to rank multiple resumes based on their match scores.
-   **Advanced NLP Models**: Integrate more sophisticated NLP models (e.g., spaCy, BERT embeddings) for better semantic understanding and more accurate matching.
-   **Bias Detection and Mitigation**: Introduce features to identify and reduce bias in screening.
-   **Keyword Extraction**: Extract key skills and keywords from both resumes and job descriptions.
-   **User Authentication**: Add user login and management features.
-   **Database Integration**: Store job descriptions, resumes, and match results in a database.
