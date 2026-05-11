from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_file):
    text = ""

    reader = PdfReader(pdf_file)

    for page in reader.pages:
        text += page.extract_text()

    return text
