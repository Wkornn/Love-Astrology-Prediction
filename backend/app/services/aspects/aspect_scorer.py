"""Aspect Scorer - Evaluates aspect quality for natal chart analysis"""

from typing import Dict, List
from .aspect_detector import DetectedAspect, AspectType

class AspectScorer:
    """
    Scores aspects based on their nature (harmonious vs challenging)
    Designed for natal chart interpretation
    """
    
    # Aspect quality scores (-1 = challenging, 0 = neutral, +1 = harmonious)
    ASPECT_QUALITY = {
        AspectType.CONJUNCTION: 0.0,   # Neutral (depends on planets involved)
        AspectType.TRINE: 1.0,          # Harmonious
        AspectType.SEXTILE: 0.7,        # Harmonious (weaker)
        AspectType.SQUARE: -0.8,        # Challenging
        AspectType.OPPOSITION: -0.6     # Challenging (but can be balancing)
    }
    
    # Planet pair compatibility modifiers for conjunctions
    CONJUNCTION_MODIFIERS = {
        ('Sun', 'Moon'): 1.0,      # Excellent
        ('Venus', 'Mars'): 0.9,    # Passionate
        ('Moon', 'Venus'): 0.8,    # Emotional harmony
        ('Sun', 'Venus'): 0.7,     # Warm
        ('Mars', 'Mars'): -0.5,    # Competitive
        ('Moon', 'Moon'): 0.6,     # Emotional understanding
    }
    
    def __init__(self):
        pass
    
    def score_aspect(self, aspect: DetectedAspect) -> float:
        """
        Score a single aspect
        
        Args:
            aspect: DetectedAspect object
            
        Returns:
            Score from -1.0 (very challenging) to +1.0 (very harmonious)
        """
        base_score = self.ASPECT_QUALITY.get(aspect.aspect_type, 0.0)
        
        # Apply strength multiplier (exact aspects are stronger)
        weighted_score = base_score * aspect.strength
        
        # Special handling for conjunctions
        if aspect.aspect_type == AspectType.CONJUNCTION:
            weighted_score = self._score_conjunction(aspect)
        
        return weighted_score
    
    def _score_conjunction(self, aspect: DetectedAspect) -> float:
        """
        Score conjunction based on planet pair
        
        Conjunctions can be harmonious or challenging depending on planets
        """
        planet_a = aspect.planet_a
        planet_b = aspect.planet_b
        
        # Check both orderings
        pair = (planet_a, planet_b)
        reverse_pair = (planet_b, planet_a)
        
        modifier = self.CONJUNCTION_MODIFIERS.get(
            pair, 
            self.CONJUNCTION_MODIFIERS.get(reverse_pair, 0.3)  # Default: slightly positive
        )
        
        return modifier * aspect.strength
    
    def score_aspect_list(self, aspects: List[DetectedAspect]) -> Dict[str, float]:
        """
        Score a list of aspects and provide breakdown
        
        Args:
            aspects: List of DetectedAspect objects
            
        Returns:
            Dictionary with scoring breakdown:
            {
                'total_score': float,
                'harmonious_count': int,
                'challenging_count': int,
                'neutral_count': int,
                'average_strength': float
            }
        """
        if not aspects:
            return {
                'total_score': 0.0,
                'harmonious_count': 0,
                'challenging_count': 0,
                'neutral_count': 0,
                'average_strength': 0.0
            }
        
        total_score = 0.0
        harmonious = 0
        challenging = 0
        neutral = 0
        total_strength = 0.0
        
        for aspect in aspects:
            score = self.score_aspect(aspect)
            total_score += score
            total_strength += aspect.strength
            
            if score > 0.2:
                harmonious += 1
            elif score < -0.2:
                challenging += 1
            else:
                neutral += 1
        
        return {
            'total_score': round(total_score, 2),
            'harmonious_count': harmonious,
            'challenging_count': challenging,
            'neutral_count': neutral,
            'average_strength': round(total_strength / len(aspects), 2)
        }
    
    def categorize_aspects_by_planet_pair(self, aspects: List[DetectedAspect]) -> Dict[str, List[DetectedAspect]]:
        """
        Group aspects by planet pair for detailed analysis
        
        Returns:
            Dictionary mapping planet pairs to their aspects
        """
        categorized = {}
        
        for aspect in aspects:
            key = f"{aspect.planet_a} - {aspect.planet_b}"
            if key not in categorized:
                categorized[key] = []
            categorized[key].append(aspect)
        
        return categorized
    
    def get_strongest_aspects(self, aspects: List[DetectedAspect], top_n: int = 5) -> List[DetectedAspect]:
        """
        Get the strongest aspects by strength score
        
        Args:
            aspects: List of aspects
            top_n: Number of top aspects to return
            
        Returns:
            List of strongest aspects
        """
        sorted_aspects = sorted(aspects, key=lambda a: a.strength, reverse=True)
        return sorted_aspects[:top_n]
