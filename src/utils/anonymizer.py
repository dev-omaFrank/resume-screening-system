# Resume Anonymization (FROZEN - DO NOT MODIFY)
import re

def anonymize_resume(text):
    """
    Anonymize resume by removing PII.

    Args:
        text: Raw resume text

    Returns:
        str: Anonymized text
    """
    # Remove emails
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)

    # Remove phone numbers
    text = re.sub(r'\d{3}[-.]?\d{3}[-.]?\d{4}', '[PHONE]', text)

    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '[URL]', text)

    return text
