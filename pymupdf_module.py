import fitz
import pandas as pd 
import os
import logging


logger = logging.getLogger(__name__)

def get_document_name(path): 
    pdf_document = fitz.open(path)
    pdf_name = pdf_document.name
    pdf_document.close()
    return pdf_name

def get_pdf_documents(path): 
    return 

def save_pdf_document(path, pdf_document): 
    
    base_name = os.path.basename(path)
    pdf_base_filename, _ = os.path.splitext(base_name)
    pdf_directory  = os.path.dirname(path)
    temp_pdf_path = os.path.join(pdf_directory, f"no_table_{pdf_base_filename}.pdf")
    pdf_document.save(temp_pdf_path)
    pdf_document.close()
    return temp_pdf_path

def get_pdf_text(path):
    pdf_document = fitz.open(path)
    pdf_text = ""
    for page in pdf_document:
        pdf_text += page.get_text()
    pdf_document.close()
    return pdf_text

def extract_pdf_images_page_by_page(path):

    return 

def extract_pdf_text_page(path, page_number):
    pdf_document = fitz.open(path)
    page = pdf_document.load_page(page_number)
    text = page.get_text().strip()
    pdf_document.close()
    return text

def extract_pdf_table_page(path, page_num):
    table_texts = []
    pages = []

    pdf_document = fitz.open(path)
    page = pdf_document.load_page(page_num)
    tables = page.find_tables()
    num_of_tables = len(tables.tables)
    if num_of_tables != 0:    
        for table in tables:
            df = pd.DataFrame(table.extract()) 
            to_html = df.to_html(index=False)
            table_texts.append(to_html)
            pages.append(page_num)
            page.add_redact_annot(table.bbox)
            page.apply_redactions()
    base_name = os.path.basename(path)
    pdf_base_filename, _ = os.path.splitext(base_name)
    pdf_directory  = os.path.dirname(path)
    temp_pdf_path = os.path.join(pdf_directory, f"no_table_{pdf_base_filename}.pdf")
    pdf_document.save(temp_pdf_path)
    pdf_document.close()
    return temp_pdf_path, num_of_tables, table_texts, pages

def extract_all_table_from_pdf(path, document_collection_id): 
    table_texts = []
    pages = []
    pdf_document = fitz.open(path)
    for page_num in range(pdf_document.page_count):
        
        page = pdf_document.load_page(page_num)
        tables = page.find_tables()
        num_of_tables = len(tables.tables)
        if num_of_tables != 0:    
            for table in tables:
                df = pd.DataFrame(table.extract()) 
                to_html = df.to_html(index=False)
                table_texts.append(to_html)
                pages.append(page_num)
                page.add_redact_annot(table.bbox)
                page.apply_redactions()
        else: 
            logger.debug(f"No tables on page {page_num}")
    base_name = os.path.basename(path)
    pdf_base_filename, _ = os.path.splitext(base_name)
    pdf_directory  = os.path.dirname(path)
    temp_pdf_path = os.path.join(pdf_directory, f"no_table_{pdf_base_filename}.pdf")
    pdf_document.save(temp_pdf_path)
    pdf_document.close()
    return temp_pdf_path, table_texts, pages

def extract_pdf_image_page(path): 
    return

def get_pdf_page_count(path):
    pdf_document = fitz.open(path)
    page_count = pdf_document.page_count
    pdf_document.close()
    return page_count   
    
def get_pdf_toc(path): 
    pdf_document = fitz.open(path)
    toc = pdf_document.get_toc()
    pdf_document.close()
    return toc

def get_page_pixmap(path, page_number):
    pdf_document = fitz.open(path)
    page = pdf_document.load_page(page_number)
    pix = page.get_pixmap()  
    width, height, samples = pix.width, pix.height, pix.samples
    pdf_document.close()
    return width, height, samples

def get_pdf_metadata(path): 
    pdf_document = fitz.open(path)
    metadata = pdf_document.metadata
    pdf_document.close()
    return metadata

def extract_pdf_text_for_metadata(path):
    pdf_document = fitz.open(path)
    doc_content = ""
    for page_num in range(min(20, len(pdf_document))):
        page = pdf_document[page_num]
        doc_content += page.get_text()
    pdf_document.close()
    return doc_content

def is_pdf_structured(path): 
    doc = fitz.open(path)
    for page in doc:
        if page.get_text("dict").get("blocks"):
            for block in page.get_text("dict")["blocks"]:
                if "title" in str(block.get("type", "")).lower():
                    return True
    doc.close()
    return False
