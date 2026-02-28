"""Compatibility Aggregator - Combines vector similarity with rule-based scoring"""

from typing import Dict, List, Optional

class CompatibilityAggregator:
    """
    Aggregates multiple compatibility signals into final score
    
    Combines:
    - Vector similarity (cosine similarity between feature vectors)
    - Rule-based scoring (astrological compatibility rules)
    
    Formula: final_score = (similarity * w1) + (rules * w2)
    """
    
    def __init__(self, similarity_weight: float = 0.6, rules_weight: float = 0.4):
        """
        Initialize aggregator with configurable weights
        
        Args:
            similarity_weight: Weight for vector similarity (default: 0.6)
            rules_weight: Weight for rule-based score (default: 0.4)
        """
        if abs(similarity_weight + rules_weight - 1.0) > 0.01:
            raise ValueError("Weights must sum to 1.0")
        
        self.similarity_weight = similarity_weight
        self.rules_weight = rules_weight
    
    def calculate_rule_based_score(self, vector1: Dict[str, float], 
                                   vector2: Dict[str, float]) -> float:
        """
        Calculate rule-based compatibility score from feature vectors
        
        Rules:
        - Venus-Mars harmony (both vectors)
        - Sun-Moon balance compatibility
        - Element compatibility
        - Emotional stability match
        
        Args:
            vector1: First person's feature dictionary
            vector2: Second person's feature dictionary
            
        Returns:
            Score 0-100
        """
        score = 0.0
        
        # Rule 1: Venus-Mars harmony (25 points)
        venus_mars_avg = (vector1['venus_mars_harmony'] + vector2['venus_mars_harmony']) / 2
        score += venus_mars_avg * 25
        
        # Rule 2: Sun-Moon balance (20 points)
        sun_moon_avg = (vector1['sun_moon_balance'] + vector2['sun_moon_balance']) / 2
        score += sun_moon_avg * 20
        
        # Rule 3: Emotional stability compatibility (20 points)
        moon_diff = abs(vector1['moon_stability'] - vector2['moon_stability'])
        moon_compat = 1.0 - moon_diff
        score += moon_compat * 20
        
        # Rule 4: Aspect quality harmony (15 points)
        aspect_avg = (vector1['aspect_quality'] + vector2['aspect_quality']) / 2
        score += aspect_avg * 15
        
        # Rule 5: 7th house strength (10 points)
        house_avg = (vector1['seventh_house_strength'] + vector2['seventh_house_strength']) / 2
        score += house_avg * 10
        
        # Rule 6: Hard/soft aspect balance (10 points)
        hard_diff = abs(vector1['hard_aspect_density'] - vector2['hard_aspect_density'])
        soft_diff = abs(vector1['soft_aspect_density'] - vector2['soft_aspect_density'])
        balance = 1.0 - ((hard_diff + soft_diff) / 2)
        score += balance * 10
        
        return round(score, 2)
    
    def calculate_emotional_sync(self, vector1: Dict[str, float], 
                                 vector2: Dict[str, float]) -> float:
        """
        Calculate emotional synchronization score
        
        Based on:
        - Moon stability match
        - Water element compatibility
        - Sun-Moon balance
        """
        moon_match = 1.0 - abs(vector1['moon_stability'] - vector2['moon_stability'])
        water_match = 1.0 - abs(vector1['water_score'] - vector2['water_score'])
        sun_moon_avg = (vector1['sun_moon_balance'] + vector2['sun_moon_balance']) / 2
        
        emotional_sync = (moon_match * 0.4 + water_match * 0.3 + sun_moon_avg * 0.3) * 100
        return round(emotional_sync, 2)
    
    def calculate_chemistry_index(self, vector1: Dict[str, float], 
                                  vector2: Dict[str, float]) -> float:
        """
        Calculate romantic/sexual chemistry index
        
        Based on:
        - Venus-Mars harmony
        - Fire element (passion)
        - 7th house strength
        """
        venus_mars_avg = (vector1['venus_mars_harmony'] + vector2['venus_mars_harmony']) / 2
        fire_avg = (vector1['fire_score'] + vector2['fire_score']) / 2
        house_avg = (vector1['seventh_house_strength'] + vector2['seventh_house_strength']) / 2
        
        chemistry = (venus_mars_avg * 0.5 + fire_avg * 0.3 + house_avg * 0.2) * 100
        return round(chemistry, 2)
    
    def calculate_stability_index(self, vector1: Dict[str, float], 
                                  vector2: Dict[str, float]) -> float:
        """
        Calculate relationship stability index
        
        Based on:
        - Earth element (grounding)
        - Fixed modality (persistence)
        - Soft aspect density (harmony)
        """
        earth_avg = (vector1['earth_score'] + vector2['earth_score']) / 2
        fixed_avg = (vector1['fixed_score'] + vector2['fixed_score']) / 2
        soft_avg = (vector1['soft_aspect_density'] + vector2['soft_aspect_density']) / 2
        
        stability = (earth_avg * 0.4 + fixed_avg * 0.4 + soft_avg * 0.2) * 100
        return round(stability, 2)
    
    def aggregate_compatibility(self, similarity_score: float, 
                               vector1: Dict[str, float], 
                               vector2: Dict[str, float]) -> Dict:
        """
        Aggregate all compatibility signals into final score
        
        Args:
            similarity_score: Cosine similarity (0-100)
            vector1: First person's feature dictionary
            vector2: Second person's feature dictionary
            
        Returns:
            {
                'overall_score': 0-100,
                'vector_component': value,
                'rule_component': value,
                'emotional_sync': value,
                'chemistry_index': value,
                'stability_index': value,
                'weights': {'similarity': w1, 'rules': w2}
            }
        """
        # Calculate rule-based score
        rule_score = self.calculate_rule_based_score(vector1, vector2)
        
        # Weighted combination
        overall = (
            similarity_score * self.similarity_weight + 
            rule_score * self.rules_weight
        )
        
        # Calculate sub-indices
        emotional_sync = self.calculate_emotional_sync(vector1, vector2)
        chemistry = self.calculate_chemistry_index(vector1, vector2)
        stability = self.calculate_stability_index(vector1, vector2)
        
        return {
            'overall_score': round(overall, 2),
            'vector_component': round(similarity_score, 2),
            'rule_component': round(rule_score, 2),
            'emotional_sync': emotional_sync,
            'chemistry_index': chemistry,
            'stability_index': stability,
            'weights': {
                'similarity': self.similarity_weight,
                'rules': self.rules_weight
            }
        }
    
    def interpret_single_chart(self, vector: Dict[str, float]) -> Dict:
        """
        Interpret single natal chart (Mode 1: no comparison)
        
        Uses weighted engineering formula for balanced scoring:
        - Element balance (30%)
        - Venus-Mars harmony (25%)
        - Moon stability (20%)
        - Aspect quality (25%)
        
        Args:
            vector: Feature dictionary from single chart
            
        Returns:
            {
                'love_readiness': 0-100,
                'emotional_maturity': 0-100,
                'relationship_focus': 0-100,
                'passion_level': 0-100,
                'stability_potential': 0-100
            }
        """
        # Calculate element balance (0-1)
        element_scores = [vector['fire_score'], vector['earth_score'], 
                         vector['air_score'], vector['water_score']]
        element_balance = 1.0 - (max(element_scores) - min(element_scores))  # Less spread = better balance
        
        # Love readiness: Weighted formula
        love_readiness = (
            element_balance * 0.30 +
            vector['venus_mars_harmony'] * 0.25 +
            vector['seventh_house_strength'] * 0.25 +
            vector['soft_aspect_density'] * 0.20
        ) * 100
        
        # Emotional maturity: Weighted formula
        emotional_maturity = (
            vector['moon_stability'] * 0.40 +
            vector['aspect_quality'] * 0.30 +
            vector['sun_moon_balance'] * 0.30
        ) * 100
        
        # Relationship focus: Weighted formula
        relationship_focus = (
            vector['seventh_house_strength'] * 0.50 +
            vector['soft_aspect_density'] * 0.30 +
            vector['venus_mars_harmony'] * 0.20
        ) * 100
        
        # Passion level: Weighted formula
        passion_level = (
            vector['fire_score'] * 0.40 +
            vector['venus_mars_harmony'] * 0.35 +
            vector['mars_element'] * 0.25
        ) * 100
        
        # Stability potential: Weighted formula
        stability_potential = (
            vector['earth_score'] * 0.35 +
            vector['fixed_score'] * 0.35 +
            vector['moon_stability'] * 0.30
        ) * 100
        
        return {
            'love_readiness': round(love_readiness, 2),
            'emotional_maturity': round(emotional_maturity, 2),
            'relationship_focus': round(relationship_focus, 2),
            'passion_level': round(passion_level, 2),
            'stability_potential': round(stability_potential, 2)
        }
