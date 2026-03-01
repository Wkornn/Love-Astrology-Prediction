"""API Response Schemas - Pydantic models for response formatting"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime

class DiagnosticItem(BaseModel):
    """Single diagnostic item"""
    code: str
    severity: Literal["CRITICAL", "WARNING", "INFO"]
    message: str
    recommendation: str

class DiagnosticsSection(BaseModel):
    """Diagnostics section for all responses"""
    bugs: List[DiagnosticItem] = []
    system_status: Optional[str] = None
    drama_risk_level: Optional[str] = None
    recommendation_summary: Optional[str] = None

class Mode1Data(BaseModel):
    """Mode 1 data section"""
    love_profile: Dict[str, float]
    personality_vector: Dict[str, float]
    narrative: Optional[Dict[str, str]] = None
    debug: Optional[Dict[str, Any]] = None

class CelebrityMatch(BaseModel):
    """Single celebrity match result"""
    name: str
    occupation: Optional[str]
    similarity_score: float
    match_reason: str
    narrative: Optional[Dict[str, str]] = None

class Mode2Data(BaseModel):
    """Mode 2 data section"""
    matches: List[CelebrityMatch]
    user_vector: Dict[str, float]
    total_celebrities: int

class Mode3Data(BaseModel):
    """Mode 3 data section"""
    overall_score: float
    vector_component: float
    rule_component: float
    emotional_sync: float
    chemistry_index: float
    stability_index: float
    strengths: List[str]
    challenges: List[str]
    narrative: Optional[Dict[str, str]] = None

class StandardResponse(BaseModel):
    """Standardized response format for all modes"""
    status: Literal["success", "error"]
    mode: Literal["mode1", "mode2", "mode3"]
    data: Dict[str, Any]
    diagnostics: DiagnosticsSection
    timestamp: str

class Mode1Response(StandardResponse):
    """Mode 1: Love reading response"""
    mode: Literal["mode1"] = "mode1"
    data: Mode1Data

class Mode2Response(StandardResponse):
    """Mode 2: Celebrity matching response"""
    mode: Literal["mode2"] = "mode2"
    data: Mode2Data

class Mode3Response(StandardResponse):
    """Mode 3: Couple compatibility response"""
    mode: Literal["mode3"] = "mode3"
    data: Mode3Data

class ErrorResponse(BaseModel):
    """Standardized error response"""
    status: Literal["error"] = "error"
    mode: Optional[str] = None
    error: str
    details: Optional[str] = None
    timestamp: str
