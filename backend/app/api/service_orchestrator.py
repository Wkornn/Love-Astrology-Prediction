"""Service Orchestrator - Business logic for all modes"""

from typing import Dict, List, Tuple
import logging
from ..services.chart.birth_chart import BirthChartCalculator
from ..services.aspects.aspect_detector import AspectDetector
from ..services.aspects.aspect_scorer import AspectScorer
from ..services.vector.feature_vector_builder import FeatureVectorBuilder
from ..services.vector.similarity_engine import SimilarityEngine
from ..services.compatibility.compatibility_aggregator import CompatibilityAggregator
from ..services.intelligence.humor_intelligence import HumorIntelligence
from ..services.intelligence.narrative_engine import NarrativeEngine
from ..database.public_figure_db import PublicFigureDatabase

logger = logging.getLogger(__name__)

class ServiceOrchestrator:
    """
    Orchestrates all services for mode execution
    No business logic in API endpoints - all here
    """
    
    def __init__(self, db_path: str = None):
        self.chart_calculator = BirthChartCalculator()
        self.aspect_detector = AspectDetector()
        self.aspect_scorer = AspectScorer()
        self.vector_builder = FeatureVectorBuilder()
        self.similarity_engine = SimilarityEngine()
        self.compatibility_aggregator = CompatibilityAggregator()
        self.humor_intelligence = HumorIntelligence()
        self.narrative_engine = NarrativeEngine()
        self.figure_db = PublicFigureDatabase(db_path)
    
    def _calculate_chart_and_vector(self, birth_data: Dict) -> Tuple[Dict, Dict]:
        """
        Calculate birth chart and feature vector with fallback
        
        Returns:
            (chart_data, vector_data)
            
        Note: Returns graceful fallback if Swiss Ephemeris fails (Demo Safety Mode)
        """
        try:
            # Calculate chart
            chart = self.chart_calculator.calculate_chart_json(
                date=birth_data['date'],
                time=birth_data['time'],
                latitude=birth_data['latitude'],
                longitude=birth_data['longitude'],
                timezone=birth_data.get('timezone', 'UTC')
            )
            
            if not chart['success']:
                logger.error(f"Chart calculation failed: {chart.get('error')}")
                return self._get_fallback_chart_and_vector()
            
            # Detect aspects
            planets = {p['name']: p['longitude'] for p in chart['data']['planets']}
            aspects = self.aspect_detector.detect_aspects(planets)
            scores = self.aspect_scorer.score_aspect_list(aspects)
            
            # Build vector
            vector_data = self.vector_builder.build_vector(
                chart['data'],
                {'aspects': [a.to_dict() for a in aspects], 'scores': scores}
            )
            
            return chart['data'], vector_data
            
        except Exception as e:
            logger.error(f"Chart/vector calculation failed: {e}, using fallback")
            return self._get_fallback_chart_and_vector()
    
    def _get_fallback_chart_and_vector(self) -> Tuple[Dict, Dict]:
        """
        Generate fallback chart and vector for demo safety
        
        Returns balanced/neutral values when calculation fails
        """
        logger.warning("Using fallback chart and vector (Demo Safety Mode)")
        
        fallback_chart = {
            'planets': [],
            'houses': {'cusps': [], 'ascendant': {}, 'midheaven': {}}
        }
        
        fallback_vector = {
            'feature_vector': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'feature_dict': {
                'venus_mars_harmony': 0.5,
                'sun_moon_balance': 0.5,
                'moon_stability': 0.5,
                'fire_score': 0.5,
                'earth_score': 0.5,
                'air_score': 0.5,
                'water_score': 0.5,
                'hard_aspect_density': 0.5,
                'soft_aspect_density': 0.5,
                'seventh_house_strength': 0.5,
                'venus_element': 0.5,
                'mars_element': 0.5,
                'aspect_quality': 0.5,
                'fixed_score': 0.5,
                'cardinal_score': 0.5,
                'mutable_score': 0.5
            }
        }
        
        return fallback_chart, fallback_vector
    
    def execute_mode1(self, birth_data: Dict, debug: bool = False) -> Dict:
        """
        Mode 1: Single-person love reading
        
        Returns natal love analysis without comparison
        """
        chart_data, vector_data = self._calculate_chart_and_vector(birth_data)
        
        # Interpret single chart
        love_profile = self.compatibility_aggregator.interpret_single_chart(
            vector_data['feature_dict']
        )
        
        # Generate humor/diagnostic layer
        diagnostics = self.humor_intelligence.analyze_single_chart(
            love_profile,
            vector_data['feature_dict']
        )
        
        # Generate LLM narrative
        narrative = self.narrative_engine.generate_mode1_narrative({
            **love_profile,
            **vector_data['feature_dict']
        })
        
        result = {
            'success': True,
            'mode': 'mode1',
            'love_profile': love_profile,
            'personality_vector': vector_data['feature_dict'],
            'narrative': narrative,
            'diagnostics': diagnostics if diagnostics else {}
        }
        
        # Add debug info if requested
        if debug:
            aspects_data = vector_data.get('aspects_data', {})
            result['debug'] = {
                'raw_feature_vector': vector_data['feature_vector'],
                'feature_labels': self.vector_builder.FEATURE_LABELS,
                'vector_length': len(vector_data['feature_vector']),
                'aspects': aspects_data.get('aspects', []),
                'aspect_scores': aspects_data.get('scores', {}),
                'chart_data': chart_data
            }
        
        return result
    
    def execute_mode2(self, birth_data: Dict, top_n: int = 5, debug: bool = False) -> Dict:
        """
        Mode 2: Celebrity matching
        
        Match user against all public figures in database
        """
        _, vector_data = self._calculate_chart_and_vector(birth_data)
        
        # Match against celebrities
        def similarity_func(vec1, vec2):
            result = self.similarity_engine.calculate_cosine_similarity(vec1, vec2)
            return result['percentage']
        
        matches = self.figure_db.match_user_to_all(
            vector_data['feature_vector'],
            similarity_func,
            top_n=top_n
        )
        
        # Format matches
        formatted_matches = []
        for figure, score in matches:
            # Generate narrative for this match
            celeb_vector_dict = dict(zip(self.vector_builder.FEATURE_LABELS, figure.get('feature_vector', [])))
            narrative = self.narrative_engine.generate_mode2_narrative(
                figure['name'],
                score,
                vector_data['feature_dict'],
                celeb_vector_dict,
                figure.get('occupation')  # Pass category/occupation
            )
            
            formatted_matches.append({
                'name': figure['name'],
                'occupation': figure.get('occupation'),
                'similarity_score': score,
                'match_reason': self._generate_match_reason(
                    vector_data['feature_dict'],
                    figure.get('feature_vector', [])
                ),
                'narrative': narrative
            })
        
        stats = self.figure_db.get_stats()
        
        result = {
            'success': True,
            'mode': 'mode2',
            'matches': formatted_matches,
            'user_vector': vector_data['feature_dict'],
            'total_celebrities': stats['total_figures']
        }
        
        # Add debug info if requested
        if debug:
            result['debug'] = {
                'raw_feature_vector': vector_data['feature_vector'],
                'feature_labels': self.vector_builder.FEATURE_LABELS,
                'raw_similarity_scores': [score for _, score in matches]
            }
        
        return result
    
    def execute_mode3(self, person1_data: Dict, person2_data: Dict, debug: bool = False) -> Dict:
        """
        Mode 3: Couple compatibility
        
        Compare two people for relationship compatibility
        """
        # Calculate both charts
        _, vector1_data = self._calculate_chart_and_vector(person1_data)
        _, vector2_data = self._calculate_chart_and_vector(person2_data)
        
        # Calculate similarity
        similarity_result = self.similarity_engine.calculate_cosine_similarity(
            vector1_data['feature_vector'],
            vector2_data['feature_vector']
        )
        
        # Aggregate compatibility
        compatibility = self.compatibility_aggregator.aggregate_compatibility(
            similarity_result['percentage'],
            vector1_data['feature_dict'],
            vector2_data['feature_dict']
        )
        
        # Analyze strengths and challenges
        strengths, challenges = self._analyze_relationship(
            vector1_data['feature_dict'],
            vector2_data['feature_dict'],
            compatibility
        )
        
        # Generate humor/diagnostic layer
        diagnostics = self.humor_intelligence.analyze_compatibility(
            compatibility['overall_score'],
            (vector1_data['feature_dict']['hard_aspect_density'] + 
             vector2_data['feature_dict']['hard_aspect_density']) / 2,
            (vector1_data['feature_dict']['moon_stability'] + 
             vector2_data['feature_dict']['moon_stability']) / 2
        )
        
        # Generate LLM narrative
        narrative = self.narrative_engine.generate_mode3_narrative({
            'overall_score': compatibility['overall_score'],
            'emotional_sync': compatibility['emotional_sync'],
            'chemistry_index': compatibility['chemistry_index'],
            'stability_index': compatibility['stability_index'],
            'hard_aspect_density': (vector1_data['feature_dict']['hard_aspect_density'] + 
                                   vector2_data['feature_dict']['hard_aspect_density']) / 2
        })
        
        result = {
            'success': True,
            'mode': 'mode3',
            'overall_score': compatibility['overall_score'],
            'vector_component': compatibility['vector_component'],
            'rule_component': compatibility['rule_component'],
            'emotional_sync': compatibility['emotional_sync'],
            'chemistry_index': compatibility['chemistry_index'],
            'stability_index': compatibility['stability_index'],
            'strengths': strengths,
            'challenges': challenges,
            'narrative': narrative,
            'diagnostics': diagnostics if diagnostics else {}
        }
        
        # Add debug info if requested
        if debug:
            result['debug'] = {
                'person1_raw_vector': vector1_data['feature_vector'],
                'person2_raw_vector': vector2_data['feature_vector'],
                'feature_labels': self.vector_builder.FEATURE_LABELS,
                'cosine_similarity_raw': similarity_result['similarity_score'],
                'cosine_similarity_percentage': similarity_result['percentage'],
                'rule_based_score': compatibility.get('rule_score', 0),
                'hard_aspect_density_p1': vector1_data['feature_dict']['hard_aspect_density'],
                'hard_aspect_density_p2': vector2_data['feature_dict']['hard_aspect_density'],
                'soft_aspect_density_p1': vector1_data['feature_dict']['soft_aspect_density'],
                'soft_aspect_density_p2': vector2_data['feature_dict']['soft_aspect_density']
            }
        
        return result
    
    def _generate_match_reason(self, user_vector: Dict, celeb_vector: List) -> str:
        """Generate explanation for celebrity match"""
        if not celeb_vector:
            return "Compatible astrological profile"
        
        # Convert list to dict if needed
        if isinstance(celeb_vector, list):
            celeb_dict = dict(zip(
                self.vector_builder.FEATURE_LABELS,
                celeb_vector
            ))
        else:
            celeb_dict = celeb_vector
        
        # Find strongest similarity
        similarities = {}
        for key in user_vector:
            if key in celeb_dict:
                diff = abs(user_vector[key] - celeb_dict[key])
                similarities[key] = 1.0 - diff
        
        if not similarities:
            return "Compatible astrological profile"
        
        strongest = max(similarities, key=similarities.get)
        
        reasons = {
            'venus_mars_harmony': 'Similar romantic expression',
            'sun_moon_balance': 'Matching emotional balance',
            'moon_stability': 'Compatible emotional stability',
            'fire_score': 'Shared passionate energy',
            'earth_score': 'Similar practical approach',
            'air_score': 'Compatible communication style',
            'water_score': 'Matching emotional depth'
        }
        
        return reasons.get(strongest, 'Compatible astrological profile')
    
    def _analyze_relationship(self, vector1: Dict, vector2: Dict, 
                             compatibility: Dict) -> Tuple[List[str], List[str]]:
        """Analyze relationship strengths and challenges"""
        strengths = []
        challenges = []
        
        # Check element compatibility
        for element in ['fire_score', 'earth_score', 'air_score', 'water_score']:
            diff = abs(vector1[element] - vector2[element])
            element_name = element.replace('_score', '').capitalize()
            
            if diff < 0.2:
                strengths.append(f"Similar {element_name} energy - natural understanding")
            elif diff > 0.5:
                challenges.append(f"Different {element_name} expression - requires compromise")
        
        # Venus-Mars harmony
        if abs(vector1['venus_mars_harmony'] - vector2['venus_mars_harmony']) < 0.2:
            strengths.append("Compatible romantic and passionate expression")
        
        # Compatibility indices
        if compatibility['emotional_sync'] > 75:
            strengths.append("Strong emotional synchronization")
        elif compatibility['emotional_sync'] < 50:
            challenges.append("Emotional differences need attention")
        
        if compatibility['chemistry_index'] > 75:
            strengths.append("High romantic chemistry")
        
        if compatibility['stability_index'] < 50:
            challenges.append("Relationship stability requires work")
        
        return strengths[:3], challenges[:3]
