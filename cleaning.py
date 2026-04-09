import re

def anonymize_resume(text: str) -> str:
    text = re.sub(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "<EMAIL>",
        text
    )

    text = re.sub(
        r"\+?\d[\d\s().-]{7,}\d",
        "<PHONE>",
        text
    )

    text = re.sub(
        r"\b(Age|DOB|Date of Birth)[:\s]*\d{1,2}.*",
        "<AGE>",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\b(19|20)\d{2}\b",
        "<YEAR>",
        text
    )

    lines = text.split("\n")

    if lines:
        first_line = lines[0].strip()

        # Replace first line if it looks like a name (1–3 capitalized words)
        if re.match(r"^[A-Z][a-z]+(\s+[A-Z][a-z]+){0,2}$", first_line):
            lines[0] = "<NAME>"

    text = "\n".join(lines)
    text = re.sub(
        r"\b(Name)[:\s]+[A-Z][a-z]+(\s+[A-Z][a-z]+)*",
        "<NAME>",
        text
    )

    text = re.sub(
        r"\b(Bank|University|Company|Ltd|Inc|Corporation)\b",
        "<ORG>",
        text
    )

    text = re.sub(
        r"\b(New York|London|Lagos|Abuja)\b",
        "<GPE>",
        text
    )

    return text