"""Feature Vector Builder - Converts natal chart + aspects into numerical feature vector"""

from typing import Dict, List, Tuple
from enum import Enum

class Element(Enum):
    """Zodiac elements"""
    FIRE = 1.0
    EARTH = 0.75
    AIR = 0.5
    WATER = 0.25

class FeatureVectorBuilder:
    """
    Converts natal chart and aspect analysis into stable numerical feature vector
    
    Vector Dimensions (9 features, all normalized 0-1):
    0. Venus element score
    1. Mars element score
    2. Moon emotional stability
    3. Hard aspect density
    4. Soft aspect density
    5. 7th house strength
    6. Venus-Mars harmony
    7. Sun-Moon balance
    8. Overall aspect quality
    """
    
    ELEMENT_MAP = {
        'Aries': Element.FIRE, 'Leo': Element.FIRE, 'Sagittarius': Element.FIRE,
        'Taurus': Element.EARTH, 'Virgo': Element.EARTH, 'Capricorn': Element.EARTH,
        'Gemini': Element.AIR, 'Libra': Element.AIR, 'Aquarius': Element.AIR,
        'Cancer': Element.WATER, 'Scorpio': Element.WATER, 'Pisces': Element.WATER
    }
    
    HARD_ASPECTS = ['Square', 'Opposition']
    SOFT_ASPECTS = ['Trine', 'Sextile']
    
    FEATURE_LABELS = [
        'venus_element',
        'mars_element',
        'moon_stability',
        'hard_aspect_density',
        'soft_aspect_density',
        'seventh_house_strength',
        'venus_mars_harmony',
        'sun_moon_balance',
        'aspect_quality'
    ]
    
    @classmethod
    def get_element_score(cls, sign: str) -> float:
        """
        Get normalized element score for zodiac sign
        
        Returns:
            Float 0-1 (Fire=1.0, Earth=0.75, Air=0.5, Water=0.25)
        """
        element = cls.ELEMENT_MAP.get(sign)
        return element.value if element else 0.5
    
    @classmethod
    def calculate_moon_stability(cls, moon_sign: str, moon_house: int) -> float:
        """
        Calculate Moon emotional stability index
        
        Factors:
        - Fixed signs = more stable (0.8-1.0)
        - Cardinal signs = moderate (0.5-0.7)
        - Mutable signs = less stable (0.3-0.5)
        - 4th house placement = bonus stability
        """
        fixed_signs = ['Taurus', 'Leo', 'Scorpio', 'Aquarius']
        cardinal_signs = ['Aries', 'Cancer', 'Libra', 'Capricorn']
        
        if moon_sign in fixed_signs:
            base_stability = 0.9
        elif moon_sign in cardinal_signs:
            base_stability = 0.6
        else:  # Mutable
            base_stability = 0.4
        
        # 4th house (home/family) adds stability
        if moon_house == 4:
            base_stability = min(1.0, base_stability + 0.1)
        
        return round(base_stability, 3)
    
    @classmethod
    def calculate_aspect_density(cls, aspects: List[Dict], aspect_types: List[str]) -> float:
        """
        Calculate density of specific aspect types
        
        Args:
            aspects: List of aspect dictionaries
            aspect_types: List of aspect type names to count
            
        Returns:
            Normalized density (0-1)
        """
        if not aspects:
            return 0.0
        
        count = sum(1 for a in aspects if a.get('aspect') in aspect_types)
        
        # Normalize: 0 aspects = 0.0, 5+ aspects = 1.0
        max_expected = 5
        density = min(1.0, count / max_expected)
        
        return round(density, 3)
    
    @classmethod
    def calculate_seventh_house_strength(cls, planets: List[Dict]) -> float:
        """
        Calculate 7th house (relationships) strength indicator
        
        Factors:
        - Venus in 7th house = 1.0
        - Mars in 7th house = 0.8
        - Sun/Moon in 7th house = 0.7
        - Other planets = 0.5
        - No planets = 0.3 (baseline)
        """
        seventh_house_planets = [p for p in planets if p.get('house') == 7]
        
        if not seventh_house_planets:
            return 0.3
        
        strength_map = {
            'Venus': 1.0,
            'Mars': 0.8,
            'Sun': 0.7,
            'Moon': 0.7,
            'Mercury': 0.5,
            'Jupiter': 0.6,
            'Saturn': 0.4
        }
        
        max_strength = max(
            strength_map.get(p['name'], 0.5) 
            for p in seventh_house_planets
        )
        
        return round(max_strength, 3)
    
    @classmethod
    def calculate_venus_mars_harmony(cls, venus_sign: str, mars_sign: str) -> float:
        """
        Calculate Venus-Mars harmony score
        
        Same element = 1.0
        Compatible elements (Fire-Air, Earth-Water) = 0.7
        Incompatible = 0.3
        """
        venus_element = cls.ELEMENT_MAP.get(venus_sign)
        mars_element = cls.ELEMENT_MAP.get(mars_sign)
        
        if not venus_element or not mars_element:
            return 0.5
        
        if venus_element == mars_element:
            return 1.0
        
        # Compatible pairs
        compatible = [
            (Element.FIRE, Element.AIR), (Element.AIR, Element.FIRE),
            (Element.EARTH, Element.WATER), (Element.WATER, Element.EARTH)
        ]
        
        if (venus_element, mars_element) in compatible:
            return 0.7
        
        return 0.3
    
    @classmethod
    def calculate_sun_moon_balance(cls, sun_sign: str, moon_sign: str) -> float:
        """
        Calculate Sun-Moon emotional balance
        
        Same element = 1.0
        Compatible elements = 0.7
        Incompatible = 0.4
        """
        sun_element = cls.ELEMENT_MAP.get(sun_sign)
        moon_element = cls.ELEMENT_MAP.get(moon_sign)
        
        if not sun_element or not moon_element:
            return 0.5
        
        if sun_element == moon_element:
            return 1.0
        
        compatible = [
            (Element.FIRE, Element.AIR), (Element.AIR, Element.FIRE),
            (Element.EARTH, Element.WATER), (Element.WATER, Element.EARTH)
        ]
        
        if (sun_element, moon_element) in compatible:
            return 0.7
        
        return 0.4
    
    @classmethod
    def calculate_aspect_quality(cls, aspect_scores: Dict) -> float:
        """
        Calculate overall aspect quality score
        
        Based on harmonious vs challenging aspect ratio
        """
        harmonious = aspect_scores.get('harmonious_count', 0)
        challenging = aspect_scores.get('challenging_count', 0)
        total = harmonious + challenging
        
        if total == 0:
            return 0.5
        
        # Ratio of harmonious aspects
        quality = harmonious / total
        
        return round(quality, 3)
    
    def build_vector(self, chart_data: Dict, aspects_data: Dict = None) -> Dict:
        """
        Build complete feature vector from chart and aspects
        
        Args:
            chart_data: Birth chart data with planets
            aspects_data: Optional aspect analysis data
            
        Returns:
            {
                'feature_vector': [float, ...],
                'feature_labels': [str, ...],
                'feature_dict': {label: value, ...}
            }
        """
        planets = chart_data.get('planets', [])
        
        # Extract planet data
        planet_dict = {p['name']: p for p in planets}
        
        venus = planet_dict.get('Venus', {})
        mars = planet_dict.get('Mars', {})
        moon = planet_dict.get('Moon', {})
        sun = planet_dict.get('Sun', {})
        
        # Feature 0: Venus element
        venus_element = self.get_element_score(venus.get('sign', ''))
        
        # Feature 1: Mars element
        mars_element = self.get_element_score(mars.get('sign', ''))
        
        # Feature 2: Moon stability
        moon_stability = self.calculate_moon_stability(
            moon.get('sign', ''),
            moon.get('house', 1)
        )
        
        # Features 3-4: Aspect density
        aspects_list = aspects_data.get('aspects', []) if aspects_data else []
        hard_density = self.calculate_aspect_density(aspects_list, self.HARD_ASPECTS)
        soft_density = self.calculate_aspect_density(aspects_list, self.SOFT_ASPECTS)
        
        # Feature 5: 7th house strength
        seventh_house = self.calculate_seventh_house_strength(planets)
        
        # Feature 6: Venus-Mars harmony
        venus_mars = self.calculate_venus_mars_harmony(
            venus.get('sign', ''),
            mars.get('sign', '')
        )
        
        # Feature 7: Sun-Moon balance
        sun_moon = self.calculate_sun_moon_balance(
            sun.get('sign', ''),
            moon.get('sign', '')
        )
        
        # Feature 8: Aspect quality
        aspect_scores = aspects_data.get('scores', {}) if aspects_data else {}
        aspect_quality = self.calculate_aspect_quality(aspect_scores)
        
        # Build vector
        feature_vector = [
            venus_element,
            mars_element,
            moon_stability,
            hard_density,
            soft_density,
            seventh_house,
            venus_mars,
            sun_moon,
            aspect_quality
        ]
        
        # Build feature dictionary
        feature_dict = dict(zip(self.FEATURE_LABELS, feature_vector))
        
        return {
            'feature_vector': feature_vector,
            'feature_labels': self.FEATURE_LABELS,
            'feature_dict': feature_dict,
            'dimensions': len(feature_vector)
        }
    
    @staticmethod
    def calculate_similarity(vector1: List[float], vector2: List[float]) -> float:
        """
        Calculate similarity between two feature vectors (0-100)
        
        Uses Euclidean distance normalized to percentage
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must have same dimensions")
        
        # Calculate Euclidean distance
        distance = sum((v1 - v2) ** 2 for v1, v2 in zip(vector1, vector2)) ** 0.5
        
        # Normalize to 0-100 scale
        # Max possible distance for 9 features (0-1 range) = sqrt(9) = 3
        max_distance = len(vector1) ** 0.5
        similarity = max(0, 100 - (distance / max_distance * 100))
        
        return round(similarity, 2)
