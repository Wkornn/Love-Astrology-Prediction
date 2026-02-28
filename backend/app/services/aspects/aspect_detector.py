"""Aspect Detector - Identifies planetary aspects within natal charts"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum

class AspectType(Enum):
    """Supported aspect types with their exact angles"""
    CONJUNCTION = 0
    SQUARE = 90
    TRINE = 120
    OPPOSITION = 180
    SEXTILE = 60

@dataclass
class AspectConfig:
    """Configuration for aspect detection"""
    type: AspectType
    orb: float
    
    @property
    def angle(self) -> float:
        return self.type.value

@dataclass
class DetectedAspect:
    """Represents a detected aspect between two planets"""
    planet_a: str
    planet_b: str
    aspect_type: AspectType
    orb: float
    exact_angle: float
    strength: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'planet_a': self.planet_a,
            'planet_b': self.planet_b,
            'aspect': self.aspect_type.name.capitalize(),
            'orb': round(self.orb, 2),
            'exact_angle': round(self.exact_angle, 2),
            'strength': round(self.strength, 2)
        }

class AspectDetector:
    """
    Detects aspects between planets within a natal chart
    
    Note: Designed for single-chart analysis.
    Future extension point for synastry/composite charts.
    """
    
    DEFAULT_ASPECTS = [
        AspectConfig(AspectType.CONJUNCTION, orb=8.0),
        AspectConfig(AspectType.OPPOSITION, orb=8.0),
        AspectConfig(AspectType.TRINE, orb=6.0),
        AspectConfig(AspectType.SQUARE, orb=6.0),
        AspectConfig(AspectType.SEXTILE, orb=4.0)
    ]
    
    def __init__(self, aspect_configs: List[AspectConfig] = None):
        """
        Initialize aspect detector
        
        Args:
            aspect_configs: List of aspect configurations (uses defaults if None)
        """
        self.aspect_configs = aspect_configs or self.DEFAULT_ASPECTS
    
    @staticmethod
    def calculate_angular_distance(long1: float, long2: float) -> float:
        """
        Calculate shortest angular distance between two longitudes
        
        Args:
            long1: First longitude (0-360)
            long2: Second longitude (0-360)
            
        Returns:
            Angular distance (0-180 degrees)
        """
        diff = abs(long1 - long2)
        if diff > 180:
            diff = 360 - diff
        return diff
    
    def calculate_aspect_strength(self, orb: float, max_orb: float) -> float:
        """
        Calculate aspect strength based on orb
        
        Args:
            orb: Actual orb (deviation from exact aspect)
            max_orb: Maximum allowed orb
            
        Returns:
            Strength score (0.0 to 1.0, where 1.0 is exact)
        """
        if orb > max_orb:
            return 0.0
        return 1.0 - (orb / max_orb)
    
    def detect_aspect(self, long1: float, long2: float) -> Tuple[DetectedAspect, None]:
        """
        Detect if two planetary positions form an aspect
        
        Args:
            long1: First planet's longitude
            long2: Second planet's longitude
            
        Returns:
            DetectedAspect if aspect found, None otherwise
        """
        angular_distance = self.calculate_angular_distance(long1, long2)
        
        for config in self.aspect_configs:
            deviation = abs(angular_distance - config.angle)
            
            if deviation <= config.orb:
                strength = self.calculate_aspect_strength(deviation, config.orb)
                return config.type, deviation, strength
        
        return None, None, None
    
    def detect_aspects(self, planets: Dict[str, float]) -> List[DetectedAspect]:
        """
        Detect all aspects within a natal chart
        
        Args:
            planets: Dictionary mapping planet names to longitudes
                    e.g., {'Sun': 120.5, 'Moon': 210.3, ...}
        
        Returns:
            List of detected aspects
        """
        aspects = []
        planet_names = list(planets.keys())
        
        for i, planet_a in enumerate(planet_names):
            for planet_b in planet_names[i + 1:]:
                long_a = planets[planet_a]
                long_b = planets[planet_b]
                
                aspect_type, orb, strength = self.detect_aspect(long_a, long_b)
                
                if aspect_type is not None:
                    angular_distance = self.calculate_angular_distance(long_a, long_b)
                    
                    aspects.append(DetectedAspect(
                        planet_a=planet_a,
                        planet_b=planet_b,
                        aspect_type=aspect_type,
                        orb=orb,
                        exact_angle=angular_distance,
                        strength=strength
                    ))
        
        return aspects
    
    def detect_aspects_json(self, planets: Dict[str, float]) -> dict:
        """
        Detect aspects and return JSON-serializable output
        
        Args:
            planets: Natal chart planets {name: longitude}
        
        Returns:
            Dictionary with detected aspects
        """
        try:
            aspects = self.detect_aspects(planets)
            
            return {
                'success': True,
                'total_aspects': len(aspects),
                'aspects': [aspect.to_dict() for aspect in aspects]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
