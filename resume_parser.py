import pdfplumber

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file using pdfplumber.
    Handles errors gracefully.
    """
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        exit
    
    # Attempt to read as binary and then decode, if pdfplumber fails
    try:
        pdf_file.seek(0) # Reset file pointer
        raw_data = pdf_file.read()
        return raw_data.decode('utf-8', errors='ignore')
    except Exception as decode_e:
        print(f"Error decoding PDF as raw text: {decode_e}")
        return None

