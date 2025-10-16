import cv2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import PyPDF2
import numpy as np
import logging
from config import settings
from core.image_processor import ImageProcessor

logger = logging.getLogger(__name__)

class OCREngine:
    def __init__(self):
        self.processor = ImageProcessor()
        self.dpi = settings.OCR_DPI
        self.lang = settings.OCR_LANG
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        text = ""
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.warning(f"Direct PDF extraction failed: {e}")
        
        if len(text.strip()) < 100:
            logger.info("Scanned PDF detected - using OCR")
            text = self._ocr_pdf(file_path)
        
        return text
    
    def _ocr_pdf(self, file_path: str) -> str:
        try:
            images = convert_from_path(file_path, dpi=self.dpi)
            text = ""
            
            for i, image in enumerate(images):
                logger.info(f"OCR processing page {i+1}/{len(images)}")
                cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                processed = self.processor.preprocess_image(cv_image)
                page_text = pytesseract.image_to_string(
                    processed, lang=self.lang, config='--psm 6 --oem 3'
                )
                text += page_text + "\n"
            
            return text
        except Exception as e:
            logger.error(f"OCR PDF failed: {e}")
            raise
    
    def extract_text_from_image(self, file_path: str) -> str:
        try:
            processed = self.processor.enhance_for_ocr(file_path)
            text = pytesseract.image_to_string(
                processed, lang=self.lang, config='--psm 6 --oem 3'
            )
            return text
        except Exception as e:
            logger.error(f"Image OCR failed: {e}")
            raise
    
    def extract_text(self, file_path: str, file_type: str) -> str:
        if file_type == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_type in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self.extract_text_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")