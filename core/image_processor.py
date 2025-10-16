import cv2
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    @staticmethod
    def preprocess_image(image: np.ndarray) -> np.ndarray:
        try:
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(denoised)
            _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return binary
        except Exception as e:
            logger.error(f"Preprocessing error: {e}")
            return image
    
    @staticmethod
    def deskew_image(image: np.ndarray) -> np.ndarray:
        try:
            edges = cv2.Canny(image, 50, 150, apertureSize=3)
            lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
            
            if lines is not None:
                angles = []
                for rho, theta in lines[:, 0]:
                    angle = np.degrees(theta) - 90
                    angles.append(angle)
                
                median_angle = np.median(angles)
                
                if abs(median_angle) > 0.5:
                    (h, w) = image.shape[:2]
                    center = (w // 2, h // 2)
                    M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
                    rotated = cv2.warpAffine(image, M, (w, h), 
                                            flags=cv2.INTER_CUBIC,
                                            borderMode=cv2.BORDER_REPLICATE)
                    return rotated
            return image
        except Exception as e:
            logger.warning(f"Deskew failed: {e}")
            return image
    
    @staticmethod
    def enhance_for_ocr(image_path: str) -> np.ndarray:
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            deskewed = ImageProcessor.deskew_image(image)
            processed = ImageProcessor.preprocess_image(deskewed)
            
            return processed
        except Exception as e:
            logger.error(f"Enhancement failed: {e}")
            raise