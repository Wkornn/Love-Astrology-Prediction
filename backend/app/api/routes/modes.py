"""API Routes - Clean endpoint handlers with no business logic"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..schemas.requests import Mode1Request, Mode2Request, Mode3Request
from ..schemas.responses import (
    Mode1Response, Mode2Response, Mode3Response, ErrorResponse,
    Mode1Data, Mode2Data, Mode3Data, DiagnosticsSection, DiagnosticItem
)
from ..service_orchestrator import ServiceOrchestrator
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize service orchestrator (singleton pattern)
orchestrator = ServiceOrchestrator()

def format_diagnostics(diagnostics_data: dict) -> DiagnosticsSection:
    """Convert diagnostics dict to DiagnosticsSection"""
    bugs = [
        DiagnosticItem(**bug) for bug in diagnostics_data.get('bugs', [])
    ]
    return DiagnosticsSection(
        bugs=bugs,
        system_status=diagnostics_data.get('system_status'),
        drama_risk_level=diagnostics_data.get('drama_risk_level'),
        recommendation_summary=diagnostics_data.get('recommendation_summary')
    )

@router.post("/mode1/love-reading", response_model=Mode1Response)
async def mode1_love_reading(request: Mode1Request):
    """
    Mode 1: Single-person love reading
    
    Returns natal love analysis and personality profile
    """
    try:
        result = orchestrator.execute_mode1(
            request.birth_data.dict(),
            debug=request.debug
        )
        
        return Mode1Response(
            status="success",
            mode="mode1",
            data=Mode1Data(
                love_profile=result['love_profile'],
                personality_vector=result['personality_vector'],
                narrative=result.get('narrative'),
                debug=result.get('debug')
            ),
            diagnostics=format_diagnostics(result.get('diagnostics', {})),
            timestamp=datetime.utcnow().isoformat() + 'Z'
        )
    except Exception as e:
        logger.error(f"Mode 1 error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "mode": "mode1",
                "error": "Failed to generate love reading",
                "details": str(e),
                "timestamp": datetime.utcnow().isoformat() + 'Z'
            }
        )

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
            top_n=request.top_n,
            debug=request.debug
        )
        
        return Mode2Response(
            status="success",
            mode="mode2",
            data=Mode2Data(
                matches=result['matches'],
                user_vector=result['user_vector'],
                total_celebrities=result['total_celebrities']
            ),
            diagnostics=DiagnosticsSection(),
            timestamp=datetime.utcnow().isoformat() + 'Z'
        )
    except Exception as e:
        logger.error(f"Mode 2 error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "mode": "mode2",
                "error": "Failed to match celebrities",
                "details": str(e),
                "timestamp": datetime.utcnow().isoformat() + 'Z'
            }
        )

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
            request.person2.dict(),
            debug=request.debug
        )
        
        return Mode3Response(
            status="success",
            mode="mode3",
            data=Mode3Data(
                overall_score=result['overall_score'],
                vector_component=result['vector_component'],
                rule_component=result['rule_component'],
                emotional_sync=result['emotional_sync'],
                chemistry_index=result['chemistry_index'],
                stability_index=result['stability_index'],
                strengths=result['strengths'],
                challenges=result['challenges'],
                narrative=result.get('narrative')
            ),
            diagnostics=format_diagnostics(result.get('diagnostics', {})),
            timestamp=datetime.utcnow().isoformat() + 'Z'
        )
    except Exception as e:
        logger.error(f"Mode 3 error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "mode": "mode3",
                "error": "Failed to analyze compatibility",
                "details": str(e),
                "timestamp": datetime.utcnow().isoformat() + 'Z'
            }
        )
