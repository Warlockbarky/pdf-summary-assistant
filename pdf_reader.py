import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file. Accepts either a file path or a BytesIO object.
    """
    if isinstance(pdf_file, (str, bytes)):  # If it's a file path
        doc = fitz.open(pdf_file)
    else:  # If it's a BytesIO object
        doc = fitz.open(stream=pdf_file, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
