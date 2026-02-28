"""API Request Schemas - Pydantic models for request validation"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class BirthDataRequest(BaseModel):
    """Birth data for single person"""
    date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    time: str = Field(..., description="Birth time in HH:MM format")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")
    timezone: Optional[str] = Field("UTC", description="IANA timezone string")
    
    @validator('date')
    def validate_date(cls, v):
        from datetime import datetime
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    @validator('time')
    def validate_time(cls, v):
        if ':' not in v or len(v.split(':')) != 2:
            raise ValueError("Time must be in HH:MM format")
        return v

class Mode1Request(BaseModel):
    """Mode 1: Single-person love reading"""
    birth_data: BirthDataRequest
    debug: Optional[bool] = Field(False, description="Include debug information")

class Mode2Request(BaseModel):
    """Mode 2: Celebrity matching"""
    birth_data: BirthDataRequest
    top_n: Optional[int] = Field(5, ge=1, le=20, description="Number of top matches")
    debug: Optional[bool] = Field(False, description="Include debug information")

class Mode3Request(BaseModel):
    """Mode 3: Couple compatibility"""
    person1: BirthDataRequest
    person2: BirthDataRequest
    debug: Optional[bool] = Field(False, description="Include debug information")
