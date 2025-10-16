from sqlalchemy.orm import Session
from models.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()