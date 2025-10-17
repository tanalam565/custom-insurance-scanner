"""
PDF handling utilities
"""
from pdf2image import convert_from_path
import cv2
import numpy as np

class PDFHandler:
    """Handles PDF to image conversion"""
    
    def __init__(self, dpi=300):
        self.dpi = dpi
    
    def get_first_page(self, pdf_path):
        """Get first page of PDF as OpenCV image"""
        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=1,
                last_page=1,
                fmt='png'
            )
            
            if images:
                # Convert PIL Image to OpenCV format
                cv_image = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
                return cv_image
            else:
                raise ValueError("No pages found in PDF")
                
        except Exception as e:
            raise ValueError(f"Error converting PDF: {e}")