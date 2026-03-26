from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

def extract_text(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    elif file_path.endswith(".html") or file_path.endswith(".htm"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text()

    return text