import os

def extract_text(file_path):
    """
    Extract plain text from a PDF or DOCX file.

    Uses context managers (with statements) everywhere so file handles
    are always closed immediately after reading — this prevents Windows
    from keeping the file locked after extraction is done.
    """
    if file_path is None:
        return ""

    text = ""
    ext  = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            import pdfplumber
            # 'with' ensures pdfplumber closes its file handle when done
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    content = page.extract_text()
                    if content:
                        text += content + "\n"

        elif ext == ".docx":
            from docx import Document
            # python-docx opens and reads the whole file in one call
            doc = Document(file_path)
            for para in doc.paragraphs:
                if para.text.strip():
                    text += para.text + "\n"

        else:
            print(f"Unsupported file type: {ext}")

    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")

    return text
