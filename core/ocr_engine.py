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
        self.max_pages = getattr(settings, "MAX_OCR_PAGES", 5)  # default to 5 pages if not defined

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

        # If little to no text found, use OCR instead
        if len(text.strip()) < 100:
            logger.info("Scanned PDF detected - switching to OCR")
            text = self._ocr_pdf(file_path)

        return text

    def _ocr_pdf(self, file_path: str) -> str:
        try:
            images = convert_from_path(file_path, dpi=self.dpi)
            text = ""

            # Limit OCR to the first N pages (default 5)
            max_pages = min(self.max_pages, len(images))
            logger.info(f"OCR limited to first {max_pages} pages out of {len(images)}")

            for i, image in enumerate(images[:max_pages]):
                logger.info(f"OCR processing page {i+1}/{max_pages}")
                cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                processed = self.processor.preprocess_image(cv_image)
                page_text = pytesseract.image_to_string(
                    processed, lang=self.lang, config='--psm 6 --oem 3'
                )
                text += page_text + "\n"

            # Log skipped pages if any
            if len(images) > max_pages:
                skipped = len(images) - max_pages
                logger.info(f"Skipped OCR for remaining {skipped} pages")

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
        """
        Automatically select extraction method based on file type.
        """
        if file_type == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_type in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self.extract_text_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
