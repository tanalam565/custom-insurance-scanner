"""
Pydantic schemas for data validation and serialization
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, validator

class ExtractionRequest(BaseModel):
    """Schema for extraction request"""
    company_name: Optional[str] = None
    
class ExtractionData(BaseModel):
    """Schema for extracted insurance data"""
    insurance_company: str
    policy_number: Optional[str] = ''
    date_prepared: Optional[str] = ''
    insurer_name: Optional[str] = ''
    insurer_address: Optional[str] = ''
    insurer_city_state: Optional[str] = ''
    insurance_amount: Optional[str] = ''
    property_address: Optional[str] = ''
    effective_date: Optional[str] = ''
    expiration_date: Optional[str] = ''
    custom_fields: Optional[Dict[str, Any]] = {}
    
    class Config:
        orm_mode = True

class ExtractionResponse(BaseModel):
    """Schema for extraction response"""
    success: bool
    record_id: Optional[int] = None
    company: str
    confidence: float
    data: ExtractionData
    is_valid: bool
    validation_errors: List[str] = []
    processing_time: float
    
class RecordResponse(BaseModel):
    """Schema for record response"""
    id: int
    filename: str
    upload_date: datetime
    insurance_company: Optional[str]
    company_confidence: Optional[float]
    policy_number: Optional[str]
    date_prepared: Optional[str]
    effective_date: Optional[str]
    expiration_date: Optional[str]
    insurer_name: Optional[str]
    insurer_address: Optional[str]
    insurer_city_state: Optional[str]
    property_address: Optional[str]
    insurance_amount: Optional[str]
    extraction_status: str
    error_message: Optional[str]
    processing_time: Optional[float]
    
    class Config:
        orm_mode = True

class RecordsListResponse(BaseModel):
    """Schema for list of records response"""
    success: bool
    count: int
    records: List[RecordResponse]

class DeleteResponse(BaseModel):
    """Schema for delete response"""
    success: bool
    message: str

class ErrorResponse(BaseModel):
    """Schema for error response"""
    error: str
    details: Optional[str] = None

class ExportRequest(BaseModel):
    """Schema for export request"""
    data: List[Dict[str, Any]]
    format: str = Field(default='excel', pattern='^(excel|csv|json)$')
    
    @validator('format')
    def validate_format(cls, v):
        if v not in ['excel', 'csv', 'json']:
            raise ValueError('Format must be excel, csv, or json')
        return v

class CompanyListResponse(BaseModel):
    """Schema for supported companies list"""
    success: bool
    companies: List[str]

class SearchRequest(BaseModel):
    """Schema for search request"""
    company: Optional[str] = None
    policy: Optional[str] = None
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    timestamp: datetime
    version: str = "1.0.0"