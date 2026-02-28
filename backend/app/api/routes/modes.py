"""API Routes - Clean endpoint handlers with no business logic"""

from fastapi import APIRouter, HTTPException
from ..schemas.requests import Mode1Request, Mode2Request, Mode3Request
from ..schemas.responses import Mode1Response, Mode2Response, Mode3Response, ErrorResponse
from ..service_orchestrator import ServiceOrchestrator

router = APIRouter()

# Initialize service orchestrator (singleton pattern)
orchestrator = ServiceOrchestrator()

@router.post("/mode1/love-reading", response_model=Mode1Response)
async def mode1_love_reading(request: Mode1Request):
    """
    Mode 1: Single-person love reading
    
    Returns natal love analysis and personality profile
    """
    try:
        result = orchestrator.execute_mode1(request.birth_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/mode2/celebrity-match", response_model=Mode2Response)
async def mode2_celebrity_match(request: Mode2Request):
    """
    Mode 2: Celebrity matching
    
    Match user against public figure database
    Returns top N matches ranked by similarity
    """
    try:
        result = orchestrator.execute_mode2(
            request.birth_data.dict(),
            top_n=request.top_n
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/mode3/couple-match", response_model=Mode3Response)
async def mode3_couple_match(request: Mode3Request):
    """
    Mode 3: Couple compatibility
    
    Compare two people for relationship compatibility
    Returns detailed compatibility report
    """
    try:
        result = orchestrator.execute_mode3(
            request.person1.dict(),
            request.person2.dict()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
