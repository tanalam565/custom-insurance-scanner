from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Renters Insurance Extractor"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str = "sqlite:///./insurance.db"
    
    MAX_FILE_SIZE: int = 20 * 1024 * 1024
    ALLOWED_EXTENSIONS: set = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    UPLOAD_DIR: str = "uploads"
    EXPORT_DIR: str = "exports"
    
    TESSERACT_CMD: Optional[str] = None
    OCR_DPI: int = 300
    OCR_LANG: str = "eng"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

if settings.TESSERACT_CMD:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD