import fitz  
def extract_text_from_pdf(pdf_path, start_page):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(start_page - 1, len(doc)): 
        page = doc[page_num]
        text += page.get_text()
    return text

pdf_path = 'IndianRecipes.pdf'
start_page = 7
extracted_text = extract_text_from_pdf(pdf_path, start_page)


with open('recipes_extracted.txt', 'w', encoding='utf-8') as f:
    f.write(extracted_text)