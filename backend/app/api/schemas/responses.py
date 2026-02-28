"""API Response Schemas - Pydantic models for response formatting"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Mode1Response(BaseModel):
    """Mode 1: Love reading response"""
    success: bool
    mode: str = "mode1"
    love_profile: Dict[str, float]
    personality_vector: Dict[str, float]
    diagnostics: Optional[List[Dict]] = None
    
class CelebrityMatch(BaseModel):
    """Single celebrity match result"""
    name: str
    occupation: Optional[str]
    similarity_score: float
    match_reason: str

class Mode2Response(BaseModel):
    """Mode 2: Celebrity matching response"""
    success: bool
    mode: str = "mode2"
    matches: List[CelebrityMatch]
    user_vector: Dict[str, float]
    total_celebrities: int

class Mode3Response(BaseModel):
    """Mode 3: Couple compatibility response"""
    success: bool
    mode: str = "mode3"
    overall_score: float
    vector_component: float
    rule_component: float
    emotional_sync: float
    chemistry_index: float
    stability_index: float
    strengths: List[str]
    challenges: List[str]
    diagnostics: Optional[List[Dict]] = None

class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    details: Optional[str] = None
