"""
Configuration
"""
import os
from pathlib import Path
import shutil

class Config:
    """Application configuration"""
    
    # Base directory
    BASE_DIR = Path(__file__).parent
    
    # Upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'uploads'))
    EXPORT_FOLDER = os.getenv('EXPORT_FOLDER', str(BASE_DIR / 'exports'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'tiff', 'bmp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Tesseract - Auto-detect
    @staticmethod
    def get_tesseract_cmd():
        """Auto-detect Tesseract path"""
        # Try environment variable
        env_path = os.getenv('TESSERACT_CMD')
        if env_path and Path(env_path).exists():
            return env_path
        
        # Try system PATH
        tesseract_path = shutil.which('tesseract')
        if tesseract_path:
            return tesseract_path
        
        # Try common paths
        common_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            '/usr/bin/tesseract',
            '/usr/local/bin/tesseract',
            '/opt/homebrew/bin/tesseract',
        ]
        
        for path in common_paths:
            if Path(path).exists():
                return path
        
        return r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    TESSERACT_CMD = get_tesseract_cmd.__func__()
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///renters_data.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.EXPORT_FOLDER, exist_ok=True)