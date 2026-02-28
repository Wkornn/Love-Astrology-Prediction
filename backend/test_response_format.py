"""Test standardized API response format"""

import sys
sys.path.insert(0, '.')

from app.api.schemas.responses import (
    Mode1Response, Mode2Response, Mode3Response,
    Mode1Data, Mode2Data, Mode3Data,
    DiagnosticsSection, DiagnosticItem, CelebrityMatch
)
from datetime import datetime

def test_mode1_response():
    """Test Mode 1 standardized response"""
    response = Mode1Response(
        status="success",
        mode="mode1",
        data=Mode1Data(
            love_profile={"romantic_readiness": 0.75},
            personality_vector={"venus_mars_harmony": 0.82}
        ),
        diagnostics=DiagnosticsSection(
            bugs=[
                DiagnosticItem(
                    code="TEST_001",
                    severity="INFO",
                    message="Test message",
                    recommendation="Test recommendation"
                )
            ],
            system_status="OPTIMAL"
        ),
        timestamp=datetime.utcnow().isoformat() + 'Z'
    )
    
    assert response.status == "success"
    assert response.mode == "mode1"
    assert "love_profile" in response.data.model_dump()
    assert len(response.diagnostics.bugs) == 1
    assert response.timestamp.endswith('Z')
    print("✅ Mode 1 response format valid")

def test_mode2_response():
    """Test Mode 2 standardized response"""
    response = Mode2Response(
        status="success",
        mode="mode2",
        data=Mode2Data(
            matches=[
                CelebrityMatch(
                    name="Test Celebrity",
                    occupation="Actor",
                    similarity_score=85.5,
                    match_reason="Compatible profile"
                )
            ],
            user_vector={"venus_mars_harmony": 0.75},
            total_celebrities=10
        ),
        diagnostics=DiagnosticsSection(),
        timestamp=datetime.utcnow().isoformat() + 'Z'
    )
    
    assert response.status == "success"
    assert response.mode == "mode2"
    assert len(response.data.matches) == 1
    assert response.data.total_celebrities == 10
    print("✅ Mode 2 response format valid")

def test_mode3_response():
    """Test Mode 3 standardized response"""
    response = Mode3Response(
        status="success",
        mode="mode3",
        data=Mode3Data(
            overall_score=78.5,
            vector_component=82.0,
            rule_component=75.0,
            emotional_sync=80.0,
            chemistry_index=76.0,
            stability_index=79.0,
            strengths=["Good communication"],
            challenges=["Different values"]
        ),
        diagnostics=DiagnosticsSection(
            bugs=[],
            system_status="STABLE",
            drama_risk_level="LOW"
        ),
        timestamp=datetime.utcnow().isoformat() + 'Z'
    )
    
    assert response.status == "success"
    assert response.mode == "mode3"
    assert response.data.overall_score == 78.5
    assert len(response.data.strengths) == 1
    print("✅ Mode 3 response format valid")

def test_response_consistency():
    """Test that all responses have same top-level structure"""
    mode1 = Mode1Response(
        status="success",
        mode="mode1",
        data=Mode1Data(love_profile={}, personality_vector={}),
        diagnostics=DiagnosticsSection(),
        timestamp=datetime.utcnow().isoformat() + 'Z'
    )
    
    mode2 = Mode2Response(
        status="success",
        mode="mode2",
        data=Mode2Data(matches=[], user_vector={}, total_celebrities=0),
        diagnostics=DiagnosticsSection(),
        timestamp=datetime.utcnow().isoformat() + 'Z'
    )
    
    mode3 = Mode3Response(
        status="success",
        mode="mode3",
        data=Mode3Data(
            overall_score=0, vector_component=0, rule_component=0,
            emotional_sync=0, chemistry_index=0, stability_index=0,
            strengths=[], challenges=[]
        ),
        diagnostics=DiagnosticsSection(),
        timestamp=datetime.utcnow().isoformat() + 'Z'
    )
    
    # All should have same top-level keys
    keys1 = set(mode1.model_dump().keys())
    keys2 = set(mode2.model_dump().keys())
    keys3 = set(mode3.model_dump().keys())
    
    assert keys1 == keys2 == keys3
    assert keys1 == {'status', 'mode', 'data', 'diagnostics', 'timestamp'}
    print("✅ All responses have consistent structure")

if __name__ == "__main__":
    print("Testing Standardized API Response Format\n")
    test_mode1_response()
    test_mode2_response()
    test_mode3_response()
    test_response_consistency()
    print("\n✅ All tests passed!")
