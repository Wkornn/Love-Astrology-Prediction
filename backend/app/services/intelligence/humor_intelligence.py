"""Humor Intelligence Layer - Professional diagnostic-style analysis"""

from typing import List, Dict, Literal
from dataclasses import dataclass

BugSeverity = Literal["CRITICAL", "WARNING", "INFO"]

@dataclass
class LoveBug:
    """Love bug diagnostic report"""
    severity: BugSeverity
    code: str
    message: str
    recommendation: str

class HumorIntelligence:
    """
    Generates professional system diagnostic-style humor
    
    Tone: Engineering diagnostic, slightly witty, never childish
    """
    
    @staticmethod
    def analyze_compatibility(overall_score: float, hard_aspect_density: float,
                             emotional_stability: float) -> Dict:
        """
        Generate diagnostic report for compatibility analysis
        
        Args:
            overall_score: Overall compatibility (0-100)
            hard_aspect_density: Hard aspect density (0-1)
            emotional_stability: Emotional stability index (0-1)
            
        Returns:
            {
                'bugs': List[LoveBug],
                'drama_risk_level': str,
                'system_status': str,
                'recommendation_summary': str
            }
        """
        bugs = []
        
        # Analyze overall compatibility
        if overall_score < 40:
            bugs.append(LoveBug(
                severity="CRITICAL",
                code="COMPAT_MISMATCH_001",
                message="Low compatibility detected. System recommends friendship mode.",
                recommendation="Consider compatibility patches or relationship refactoring."
            ))
        elif overall_score < 60:
            bugs.append(LoveBug(
                severity="WARNING",
                code="COMPAT_SUBOPTIMAL_002",
                message="Moderate compatibility. Relationship may require manual optimization.",
                recommendation="Deploy communication protocols and conflict resolution handlers."
            ))
        elif overall_score >= 85:
            bugs.append(LoveBug(
                severity="INFO",
                code="COMPAT_OPTIMAL_000",
                message="High compatibility detected. System operating within optimal parameters.",
                recommendation="Maintain current configuration. Monitor for edge cases."
            ))
        
        # Analyze hard aspects (tension)
        if hard_aspect_density > 0.6:
            bugs.append(LoveBug(
                severity="CRITICAL",
                code="ASPECT_TENSION_HIGH_101",
                message="Elevated tension levels detected. Drama overflow risk imminent.",
                recommendation="Implement stress management protocols. Schedule regular system maintenance."
            ))
        elif hard_aspect_density > 0.4:
            bugs.append(LoveBug(
                severity="WARNING",
                code="ASPECT_TENSION_MOD_102",
                message="Moderate tension detected. Occasional system conflicts expected.",
                recommendation="Deploy patience buffers and compromise algorithms."
            ))
        elif hard_aspect_density < 0.2:
            bugs.append(LoveBug(
                severity="INFO",
                code="ASPECT_HARMONY_103",
                message="Low tension environment. Smooth operation likely.",
                recommendation="Maintain harmony protocols. Avoid complacency."
            ))
        
        # Analyze emotional stability
        if emotional_stability < 0.4:
            bugs.append(LoveBug(
                severity="WARNING",
                code="EMOTION_VOLATILE_201",
                message="Emotional volatility detected. Unpredictable behavior patterns likely.",
                recommendation="Implement emotional regulation middleware. Increase communication bandwidth."
            ))
        elif emotional_stability > 0.8:
            bugs.append(LoveBug(
                severity="INFO",
                code="EMOTION_STABLE_200",
                message="High emotional stability. Consistent system behavior expected.",
                recommendation="Leverage stability for long-term planning. Monitor for rigidity."
            ))
        
        # Calculate drama risk level
        drama_risk = HumorIntelligence._calculate_drama_risk(
            overall_score, hard_aspect_density, emotional_stability
        )
        
        # Generate system status
        system_status = HumorIntelligence._generate_system_status(overall_score)
        
        # Generate recommendation summary
        recommendation = HumorIntelligence._generate_recommendation(
            overall_score, hard_aspect_density, emotional_stability
        )
        
        return {
            'bugs': [
                {
                    'severity': bug.severity,
                    'code': bug.code,
                    'message': bug.message,
                    'recommendation': bug.recommendation
                }
                for bug in bugs
            ],
            'drama_risk_level': drama_risk,
            'system_status': system_status,
            'recommendation_summary': recommendation
        }
    
    @staticmethod
    def _calculate_drama_risk(overall_score: float, hard_aspect_density: float,
                              emotional_stability: float) -> str:
        """Calculate drama risk level"""
        
        # Drama risk formula
        drama_score = (
            (1 - overall_score / 100) * 0.4 +
            hard_aspect_density * 0.4 +
            (1 - emotional_stability) * 0.2
        )
        
        if drama_score > 0.7:
            return "CRITICAL - High probability of system instability"
        elif drama_score > 0.5:
            return "ELEVATED - Moderate conflict potential detected"
        elif drama_score > 0.3:
            return "MODERATE - Manageable with proper protocols"
        else:
            return "LOW - System stable, minimal intervention required"
    
    @staticmethod
    def _generate_system_status(overall_score: float) -> str:
        """Generate system status message"""
        
        if overall_score >= 85:
            return "OPTIMAL - All systems nominal. Relationship operating at peak efficiency."
        elif overall_score >= 70:
            return "STABLE - System functional. Minor optimizations recommended."
        elif overall_score >= 55:
            return "DEGRADED - Performance below optimal. Maintenance required."
        elif overall_score >= 40:
            return "UNSTABLE - Significant issues detected. Immediate attention needed."
        else:
            return "CRITICAL - System compatibility failure. Consider alternative configurations."
    
    @staticmethod
    def _generate_recommendation(overall_score: float, hard_aspect_density: float,
                                 emotional_stability: float) -> str:
        """Generate recommendation summary"""
        
        if overall_score >= 80 and hard_aspect_density < 0.3:
            return ("System analysis indicates high compatibility. "
                   "Recommended action: Proceed with confidence. "
                   "Maintain open communication channels and regular system checks.")
        
        elif overall_score >= 60 and emotional_stability > 0.6:
            return ("Moderate compatibility detected with stable emotional foundation. "
                   "Recommended action: Invest in relationship infrastructure. "
                   "Deploy conflict resolution protocols proactively.")
        
        elif hard_aspect_density > 0.6:
            return ("High tension environment detected. "
                   "Recommended action: Implement robust communication framework. "
                   "Schedule regular maintenance windows for conflict resolution.")
        
        elif emotional_stability < 0.4:
            return ("Emotional volatility detected. "
                   "Recommended action: Establish clear boundaries and expectations. "
                   "Deploy emotional support systems and patience buffers.")
        
        elif overall_score < 50:
            return ("Low compatibility score indicates significant challenges. "
                   "Recommended action: Evaluate relationship objectives. "
                   "Consider if investment justifies required maintenance overhead.")
        
        else:
            return ("Mixed signals detected. System requires careful monitoring. "
                   "Recommended action: Proceed with caution. "
                   "Implement incremental commitment strategy with regular assessments.")
    
    @staticmethod
    def analyze_single_chart(love_profile: Dict[str, float],
                            personality_vector: Dict[str, float]) -> Dict:
        """
        Generate diagnostic report for single person (Mode 1)
        
        Args:
            love_profile: Love readiness metrics
            personality_vector: Feature vector
            
        Returns:
            Diagnostic report with bugs and recommendations
        """
        bugs = []
        
        # Analyze love readiness
        readiness = love_profile.get('love_readiness', 50)
        if readiness < 50:
            bugs.append(LoveBug(
                severity="WARNING",
                code="READINESS_LOW_301",
                message="Love readiness below optimal threshold. System not fully initialized.",
                recommendation="Focus on self-development protocols before relationship deployment."
            ))
        elif readiness > 80:
            bugs.append(LoveBug(
                severity="INFO",
                code="READINESS_HIGH_300",
                message="High love readiness detected. System primed for relationship mode.",
                recommendation="Proceed with partner search. Compatibility matching recommended."
            ))
        
        # Analyze emotional maturity
        maturity = love_profile.get('emotional_maturity', 50)
        if maturity < 60:
            bugs.append(LoveBug(
                severity="WARNING",
                code="MATURITY_DEVELOPING_401",
                message="Emotional maturity in development phase. Growth potential detected.",
                recommendation="Invest in emotional intelligence upgrades. Practice self-awareness protocols."
            ))
        
        # Analyze passion vs stability balance
        passion = love_profile.get('passion_level', 50)
        stability = love_profile.get('stability_potential', 50)
        
        if passion > 80 and stability < 40:
            bugs.append(LoveBug(
                severity="WARNING",
                code="BALANCE_PASSION_HEAVY_501",
                message="High passion, low stability detected. Exciting but potentially volatile configuration.",
                recommendation="Balance passion with grounding practices. Deploy stability protocols."
            ))
        elif stability > 80 and passion < 40:
            bugs.append(LoveBug(
                severity="INFO",
                code="BALANCE_STABILITY_HEAVY_502",
                message="High stability, moderate passion. Reliable but may lack spontaneity.",
                recommendation="Introduce novelty subroutines. Schedule adventure modules."
            ))
        
        # Generate overall assessment
        avg_score = sum(love_profile.values()) / len(love_profile)
        
        if avg_score >= 75:
            status = "READY - System optimized for relationship deployment"
            recommendation = "High compatibility potential. Proceed with partner matching."
        elif avg_score >= 60:
            status = "FUNCTIONAL - System operational with minor optimizations needed"
            recommendation = "Continue self-development while exploring relationship opportunities."
        else:
            status = "DEVELOPING - System requires additional configuration"
            recommendation = "Focus on personal growth. Relationship mode not yet optimal."
        
        return {
            'bugs': [
                {
                    'severity': bug.severity,
                    'code': bug.code,
                    'message': bug.message,
                    'recommendation': bug.recommendation
                }
                for bug in bugs
            ],
            'system_status': status,
            'recommendation_summary': recommendation
        }
