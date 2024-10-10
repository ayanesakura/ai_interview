import PyPDF2

def load_pdf(pdf_path):

    # 读取PDF文件
    texts = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            texts.append(page.extract_text())
    return '\n'.join(texts)