from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import Config

Base = declarative_base()

class ExtractionRecord(Base):
    """Database model for extraction records"""
    __tablename__ = 'extraction_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Document information
    filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # Insurance company
    insurance_company = Column(String(100))
    company_confidence = Column(Float)
    
    # Policy information
    policy_number = Column(String(100))
    date_prepared = Column(String(50))
    effective_date = Column(String(50))
    expiration_date = Column(String(50))
    
    # Insurer information
    insurer_name = Column(String(200))
    insurer_address = Column(String(300))
    insurer_city_state = Column(String(150))
    
    # Property information
    property_address = Column(String(300))
    insurance_amount = Column(String(50))
    
    # Custom fields (JSON format)
    custom_fields = Column(Text)
    
    # Processing information
    extraction_status = Column(String(50), default='success')
    error_message = Column(Text)
    processing_time = Column(Float)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'insurance_company': self.insurance_company,
            'company_confidence': self.company_confidence,
            'policy_number': self.policy_number,
            'date_prepared': self.date_prepared,
            'effective_date': self.effective_date,
            'expiration_date': self.expiration_date,
            'insurer_name': self.insurer_name,
            'insurer_address': self.insurer_address,
            'insurer_city_state': self.insurer_city_state,
            'property_address': self.property_address,
            'insurance_amount': self.insurance_amount,
            'custom_fields': self.custom_fields,
            'extraction_status': self.extraction_status,
            'error_message': self.error_message,
            'processing_time': self.processing_time
        }

class Database:
    """Database manager"""
    
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        return self.Session()
    
    def save_extraction(self, data):
        """Save extraction record
        
        Args:
            data: Dictionary with extraction data
            
        Returns:
            Saved record ID
        """
        session = self.get_session()
        try:
            record = ExtractionRecord(**data)
            session.add(record)
            session.commit()
            record_id = record.id
            session.close()
            return record_id
        except Exception as e:
            session.rollback()
            session.close()
            raise e
    
    def get_extraction(self, record_id):
        """Get extraction record by ID"""
        session = self.get_session()
        record = session.query(ExtractionRecord).filter_by(id=record_id).first()
        session.close()
        return record
    
    def get_all_extractions(self, limit=100, offset=0):
        """Get all extraction records"""
        session = self.get_session()
        records = session.query(ExtractionRecord)\
            .order_by(ExtractionRecord.upload_date.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        session.close()
        return records
    
    def search_extractions(self, **kwargs):
        """Search extraction records"""
        session = self.get_session()
        query = session.query(ExtractionRecord)
        
        for key, value in kwargs.items():
            if hasattr(ExtractionRecord, key) and value:
                query = query.filter(getattr(ExtractionRecord, key).ilike(f'%{value}%'))
        
        records = query.all()
        session.close()
        return records
    
    def delete_extraction(self, record_id):
        """Delete extraction record"""
        session = self.get_session()
        try:
            record = session.query(ExtractionRecord).filter_by(id=record_id).first()
            if record:
                session.delete(record)
                session.commit()
                session.close()
                return True
            session.close()
            return False
        except Exception as e:
            session.rollback()
            session.close()
            raise e