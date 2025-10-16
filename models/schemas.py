from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class InsuranceDataResponse(BaseModel):
    policy_number: Optional[str] = None
    policyholder_name: Optional[str] = None
    property_address: Optional[str] = None
    coverage_amount: Optional[str] = None
    liability_coverage: Optional[str] = None
    deductible: Optional[str] = None
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    premium_amount: Optional[str] = None
    insurance_company: Optional[str] = None
    detected_company: Optional[str] = None
    confidence_score: float = Field(default=0.0, ge=0, le=100)
    processing_time: Optional[float] = None
    needs_review: bool = False
    
    @field_validator('confidence_score')
    @classmethod
    def validate_confidence(cls, v):
        """Ensure confidence is always between 0 and 100."""
        if v is None:
            return 0.0
        return max(0.0, min(100.0, float(v)))

class UploadResponse(BaseModel):
    success: bool
    message: str
    filename: str
    data: InsuranceDataResponse
    record_id: int

class ExportRequest(BaseModel):
    format: str = Field(..., pattern="^(excel|csv|json)$")
    record_ids: Optional[list] = None