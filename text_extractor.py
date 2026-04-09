import zipfile
import xml.etree.ElementTree as ET

def extract_text(uploaded_file):
    """
    Extract text from PDF, DOCX (without extra packages), or TXT file.
    """
    file_type = uploaded_file.type

    # --- PDF ---
    if file_type == "application/pdf":
        from resume_parser import extract_text_from_pdf
        return extract_text_from_pdf(uploaded_file)

    # --- DOCX (no external packages) ---
    elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                       "application/msword"]:
        try:
            docx_zip = zipfile.ZipFile(uploaded_file)
            xml_content = docx_zip.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            paragraphs = []
            for paragraph in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
                texts = [node.text for node in paragraph.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
                if texts:
                    paragraphs.append("".join(texts))
            return "\n".join(paragraphs)
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return None

    # --- TXT ---
    elif file_type == "text/plain":
        return uploaded_file.getvalue().decode("utf-8")

    else:
        return None