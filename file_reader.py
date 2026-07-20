"""
File Reader
------------
Extracts plain text from an uploaded resume file (.pdf, .docx, or .txt)
so the rest of the pipeline (which works on plain text) can process it.
"""
import os


def extract_text_from_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if ext == ".docx":
        import docx
        doc = docx.Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext in (".txt", ".md"):
        with open(filepath, "r", errors="ignore") as f:
            return f.read()

    raise ValueError(f"Unsupported file type: {ext}. Please upload a .pdf, .docx, or .txt file.")
