"""
PDF handling utilities for converting PDFs to images
"""
import os
import tempfile
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import cv2

class PDFHandler:
    """Handles PDF to image conversion"""
    
    def __init__(self, dpi=300):
        """
        Initialize PDF handler
        
        Args:
            dpi: Resolution for PDF conversion (higher = better quality)
        """
        self.dpi = dpi
    
    def is_pdf(self, filepath):
        """Check if file is a PDF"""
        return str(filepath).lower().endswith('.pdf')
    
    def convert_pdf_to_images(self, pdf_path, output_folder=None):
        """Convert PDF pages to images
        
        Args:
            pdf_path: Path to PDF file
            output_folder: Optional folder to save images
            
        Returns:
            List of image paths or numpy arrays
        """
        try:
            # Convert PDF to images (one per page)
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                fmt='png'
            )
            
            if output_folder:
                # Save images to folder
                output_folder = Path(output_folder)
                output_folder.mkdir(exist_ok=True)
                
                image_paths = []
                for i, image in enumerate(images):
                    image_path = output_folder / f"page_{i+1}.png"
                    image.save(image_path, 'PNG')
                    image_paths.append(image_path)
                
                return image_paths
            else:
                # Return as numpy arrays for OpenCV
                cv_images = []
                for image in images:
                    # Convert PIL Image to OpenCV format
                    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                    cv_images.append(cv_image)
                
                return cv_images
                
        except Exception as e:
            print(f"Error converting PDF: {e}")
            raise
    
    def get_first_page(self, pdf_path):
        """Get only the first page of PDF as image
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            First page as numpy array (OpenCV format)
        """
        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=1,
                last_page=1,
                fmt='png'
            )
            
            if images:
                # Convert to OpenCV format
                cv_image = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
                return cv_image
            else:
                raise ValueError("No pages found in PDF")
                
        except Exception as e:
            print(f"Error getting first page: {e}")
            raise
    
    def get_page(self, pdf_path, page_number=1):
        """Get a specific page from PDF
        
        Args:
            pdf_path: Path to PDF file
            page_number: Page number (1-indexed)
            
        Returns:
            Page as numpy array (OpenCV format)
        """
        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=page_number,
                last_page=page_number,
                fmt='png'
            )
            
            if images:
                cv_image = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
                return cv_image
            else:
                raise ValueError(f"Page {page_number} not found in PDF")
                
        except Exception as e:
            print(f"Error getting page {page_number}: {e}")
            raise
    
    def get_page_count(self, pdf_path):
        """Get number of pages in PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Number of pages
        """
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_path)
            return len(reader.pages)
        except Exception as e:
            print(f"Error getting page count: {e}")
            # Fallback: convert all pages and count
            images = convert_from_path(pdf_path, dpi=self.dpi)
            return len(images)