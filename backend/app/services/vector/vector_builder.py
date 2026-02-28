"""Vector Builder - Converts birth charts into numerical feature vectors"""

from typing import Dict, List
from enum import Enum

class ZodiacElement(Enum):
    FIRE = ['Aries', 'Leo', 'Sagittarius']
    EARTH = ['Taurus', 'Virgo', 'Capricorn']
    AIR = ['Gemini', 'Libra', 'Aquarius']
    WATER = ['Cancer', 'Scorpio', 'Pisces']

class ZodiacModality(Enum):
    CARDINAL = ['Aries', 'Cancer', 'Libra', 'Capricorn']
    FIXED = ['Taurus', 'Leo', 'Scorpio', 'Aquarius']
    MUTABLE = ['Gemini', 'Virgo', 'Sagittarius', 'Pisces']

class ChartVectorBuilder:
    """
    Converts astrological birth chart into numerical feature vector
    Used for similarity comparison and personality analysis
    """
    
    PLANET_WEIGHTS = {
        'Sun': 1.0,
        'Moon': 1.0,
        'Venus': 0.9,
        'Mars': 0.9,
        'Mercury': 0.7
    }
    
    @staticmethod
    def get_element(sign: str) -> str:
        """Get element for zodiac sign"""
        for element in ZodiacElement:
            if sign in element.value:
                return element.name
        return 'UNKNOWN'
    
    @staticmethod
    def get_modality(sign: str) -> str:
        """Get modality for zodiac sign"""
        for modality in ZodiacModality:
            if sign in modality.value:
                return modality.name
        return 'UNKNOWN'
    
    def build_vector(self, chart_data: dict) -> Dict[str, float]:
        """
        Build feature vector from birth chart
        
        Args:
            chart_data: Birth chart data with planets
            
        Returns:
            Dictionary of numerical features:
            {
                'fire_score': 0.5,
                'earth_score': 0.2,
                'air_score': 0.1,
                'water_score': 0.2,
                'cardinal_score': 0.3,
                'fixed_score': 0.4,
                'mutable_score': 0.3,
                'venus_mars_harmony': 0.8,
                'sun_moon_balance': 0.6
            }
        """
        planets = chart_data.get('planets', {})
        
        # Element distribution
        element_scores = {'FIRE': 0.0, 'EARTH': 0.0, 'AIR': 0.0, 'WATER': 0.0}
        modality_scores = {'CARDINAL': 0.0, 'FIXED': 0.0, 'MUTABLE': 0.0}
        
        total_weight = 0.0
        
        for planet_data in planets:
            planet_name = planet_data['name']
            sign = planet_data['sign']
            weight = self.PLANET_WEIGHTS.get(planet_name, 0.5)
            
            element = self.get_element(sign)
            modality = self.get_modality(sign)
            
            element_scores[element] += weight
            modality_scores[modality] += weight
            total_weight += weight
        
        # Normalize scores
        if total_weight > 0:
            for key in element_scores:
                element_scores[key] /= total_weight
            for key in modality_scores:
                modality_scores[key] /= total_weight
        
        # Calculate special metrics
        venus_mars_harmony = self._calculate_venus_mars_harmony(planets)
        sun_moon_balance = self._calculate_sun_moon_balance(planets)
        
        return {
            'fire_score': round(element_scores['FIRE'], 3),
            'earth_score': round(element_scores['EARTH'], 3),
            'air_score': round(element_scores['AIR'], 3),
            'water_score': round(element_scores['WATER'], 3),
            'cardinal_score': round(modality_scores['CARDINAL'], 3),
            'fixed_score': round(modality_scores['FIXED'], 3),
            'mutable_score': round(modality_scores['MUTABLE'], 3),
            'venus_mars_harmony': round(venus_mars_harmony, 3),
            'sun_moon_balance': round(sun_moon_balance, 3)
        }
    
    def _calculate_venus_mars_harmony(self, planets: List[dict]) -> float:
        """Calculate Venus-Mars compatibility indicator"""
        venus_sign = None
        mars_sign = None
        
        for planet in planets:
            if planet['name'] == 'Venus':
                venus_sign = planet['sign']
            elif planet['name'] == 'Mars':
                mars_sign = planet['sign']
        
        if not venus_sign or not mars_sign:
            return 0.5
        
        venus_element = self.get_element(venus_sign)
        mars_element = self.get_element(mars_sign)
        
        # Same element = high harmony
        if venus_element == mars_element:
            return 1.0
        
        # Compatible elements (Fire-Air, Earth-Water)
        compatible = [
            ('FIRE', 'AIR'), ('AIR', 'FIRE'),
            ('EARTH', 'WATER'), ('WATER', 'EARTH')
        ]
        
        if (venus_element, mars_element) in compatible:
            return 0.7
        
        return 0.3
    
    def _calculate_sun_moon_balance(self, planets: List[dict]) -> float:
        """Calculate Sun-Moon emotional balance indicator"""
        sun_sign = None
        moon_sign = None
        
        for planet in planets:
            if planet['name'] == 'Sun':
                sun_sign = planet['sign']
            elif planet['name'] == 'Moon':
                moon_sign = planet['sign']
        
        if not sun_sign or not moon_sign:
            return 0.5
        
        sun_element = self.get_element(sun_sign)
        moon_element = self.get_element(moon_sign)
        
        # Same element = balanced
        if sun_element == moon_element:
            return 1.0
        
        # Compatible elements
        compatible = [
            ('FIRE', 'AIR'), ('AIR', 'FIRE'),
            ('EARTH', 'WATER'), ('WATER', 'EARTH')
        ]
        
        if (sun_element, moon_element) in compatible:
            return 0.7
        
        return 0.4
    
    @staticmethod
    def calculate_similarity(vector1: Dict[str, float], vector2: Dict[str, float]) -> float:
        """
        Calculate similarity score between two vectors (0-100)
        
        Uses weighted Euclidean distance
        """
        weights = {
            'fire_score': 1.0,
            'earth_score': 1.0,
            'air_score': 1.0,
            'water_score': 1.0,
            'cardinal_score': 0.8,
            'fixed_score': 0.8,
            'mutable_score': 0.8,
            'venus_mars_harmony': 1.2,
            'sun_moon_balance': 1.0
        }
        
        distance = 0.0
        total_weight = 0.0
        
        for key in vector1:
            if key in vector2:
                weight = weights.get(key, 1.0)
                diff = (vector1[key] - vector2[key]) ** 2
                distance += diff * weight
                total_weight += weight
        
        # Normalize and convert to similarity (0-100)
        if total_weight > 0:
            distance = (distance / total_weight) ** 0.5
        
        similarity = max(0, 100 - (distance * 100))
        return round(similarity, 2)
