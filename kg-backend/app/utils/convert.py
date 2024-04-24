import pdfplumber
import io
import base64

def convert_pdf_to_txt(pdf_base64_string):
    pdf_bytes = base64.b64decode(pdf_base64_string)
    pdf_file = io.BytesIO(pdf_bytes)
    
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    return text
        
        