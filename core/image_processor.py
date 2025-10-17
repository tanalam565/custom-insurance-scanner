import cv2
import numpy as np
from PIL import Image, ImageEnhance
from config import Config
from core.pdf_handler import PDFHandler

class ImageProcessor:
    """Handles image preprocessing for OCR"""
    
    def __init__(self, zoom_factor=None):
        self.zoom_factor = zoom_factor or Config.ZOOM_FACTOR
        self.pdf_handler = PDFHandler()
    
    def load_image(self, image_path):
        """Load image from path (supports both images and PDFs)"""
        image_path = str(image_path)
        
        # Check if it's a PDF
        if self.pdf_handler.is_pdf(image_path):
            # Convert first page of PDF to image
            img = self.pdf_handler.get_first_page(image_path)
            if img is None:
                raise ValueError(f"Could not convert PDF from {image_path}")
            return img
        else:
            # Load regular image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image from {image_path}")
            return img
    
    def zoom_image(self, img, zoom_factor=None):
        """Zoom image by specified factor"""
        zoom = zoom_factor or self.zoom_factor
        height, width = img.shape[:2]
        new_width = int(width * zoom)
        new_height = int(height * zoom)
        return cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    def extract_roi(self, img, coords):
        """Extract region of interest from image
        
        Args:
            img: Input image
            coords: Tuple of (x, y, width, height)
        
        Returns:
            Extracted region as numpy array
        """
        x, y, w, h = coords
        return img[y:y+h, x:x+w]
    
    def preprocess_roi(self, roi):
        """Preprocess ROI for better OCR accuracy
        
        Args:
            roi: Region of interest
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold using OTSU method
        thresh = cv2.threshold(
            gray_roi, 
            0, 
            255, 
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )[1]
        
        return thresh
    
    def enhance_image(self, img):
        """Enhance image quality using PIL"""
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(pil_img)
        pil_img = enhancer.enhance(2.0)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(1.5)
        
        # Convert back to OpenCV format
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def denoise_image(self, img):
        """Remove noise from image"""
        return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    def deskew_image(self, img):
        """Correct skew in image"""
        coords = np.column_stack(np.where(img > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            img, 
            M, 
            (w, h),
            flags=cv2.INTER_CUBIC, 
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    def get_processed_roi(self, img, coords, enhance=True):
        """Complete pipeline to get processed ROI
        
        Args:
            img: Input image
            coords: Coordinates (x, y, w, h)
            enhance: Whether to apply enhancement
            
        Returns:
            Preprocessed ROI ready for OCR
        """
        roi = self.extract_roi(img, coords)
        
        if enhance:
            roi = self.enhance_image(roi)
        
        processed = self.preprocess_roi(roi)
        
        return processed