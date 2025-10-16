from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class InsuranceRecord(Base):
    __tablename__ = "insurance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    policy_number = Column(String(100))
    policyholder_name = Column(String(255))
    property_address = Column(Text)
    coverage_amount = Column(String(50))
    liability_coverage = Column(String(50))
    deductible = Column(String(50))
    effective_date = Column(String(50))
    expiration_date = Column(String(50))
    premium_amount = Column(String(50))
    insurance_company = Column(String(255))
    
    detected_company = Column(String(100))
    confidence_score = Column(Float)
    raw_text = Column(Text)
    processing_time = Column(Float)
    needs_review = Column(Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'policy_number': self.policy_number,
            'policyholder_name': self.policyholder_name,
            'property_address': self.property_address,
            'coverage_amount': self.coverage_amount,
            'liability_coverage': self.liability_coverage,
            'deductible': self.deductible,
            'effective_date': self.effective_date,
            'expiration_date': self.expiration_date,
            'premium_amount': self.premium_amount,
            'insurance_company': self.insurance_company,
            'detected_company': self.detected_company,
            'confidence_score': self.confidence_score,
            'processing_time': self.processing_time,
            'needs_review': self.needs_review,
        }

Base.metadata.create_all(bind=engine)
