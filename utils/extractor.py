import pdfplumber

def extract_text_from_pdf(file):
    """
    Takes a PDF file object and returns extracted text as string.
    """
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()