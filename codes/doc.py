from docx import Document

def read_doc(file):
    """Read a DOCX file and return its content as a string."""
    document = Document(file)
    document_text = ""
    for para in document.paragraphs:
        document_text += para.text + "\n"
    return document_text
