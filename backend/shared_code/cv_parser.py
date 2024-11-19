import os
import docx2txt
import logging
from pypdf import PdfReader

logger = logging.getLogger(__name__)

def parse_cv(file_path):
    _, file_extension = os.path.splitext(file_path)
    text = ""
    try:
        if file_extension.lower() == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            logger.debug("Parsed TXT CV successfully.")
        elif file_extension.lower() == '.pdf':
            reader = PdfReader(file_path)
            text = ""
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            logger.debug("Parsed PDF CV successfully using pypdf.")
        elif file_extension.lower() == '.docx':
            text = docx2txt.process(file_path)
            logger.debug("Parsed DOCX CV successfully.")
        else:
            logger.warning(f"Unsupported file extension: {file_extension}")
    except Exception as e:
        logger.error(f"Error parsing CV file {file_path}: {e}", exc_info=True)
    return text.strip()
