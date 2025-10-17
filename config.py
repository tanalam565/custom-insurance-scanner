import os
from pathlib import Path

class Config:
    """Application configuration"""
    
    # Base directory
    BASE_DIR = Path(__file__).parent
    
    # Upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'uploads'))
    EXPORT_FOLDER = os.getenv('EXPORT_FOLDER', str(BASE_DIR / 'exports'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'tiff', 'bmp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Tesseract configuration
    TESSERACT_CMD = os.getenv('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    TESSERACT_CONFIG = '--psm 6 -l eng'
    
    # OCR settings
    ZOOM_FACTOR = 2
    THRESHOLD_METHOD = 'OTSU'
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///renters_data.db')
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Company detection confidence threshold
    COMPANY_DETECTION_THRESHOLD = 0.7
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.EXPORT_FOLDER, exist_ok=True)