"""Planetary Calculator - High-level API for planetary positions"""

from datetime import datetime
from typing import Dict, List
from .swisseph_adapter import SwissEphemerisAdapter

class PlanetaryCalculator:
    """High-level interface for calculating planetary positions"""
    
    ZODIAC_SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    def __init__(self, ephemeris_path: str = None):
        self.adapter = SwissEphemerisAdapter(ephemeris_path)
    
    @staticmethod
    def longitude_to_sign_and_degree(longitude: float) -> tuple[str, float]:
        """
        Convert ecliptic longitude to zodiac sign and degree within sign
        
        Args:
            longitude: Ecliptic longitude (0-360 degrees)
            
        Returns:
            Tuple of (sign_name, degree_in_sign)
        """
        longitude = longitude % 360
        sign_index = int(longitude / 30)
        degree_in_sign = longitude % 30
        
        sign_name = PlanetaryCalculator.ZODIAC_SIGNS[sign_index]
        return sign_name, degree_in_sign
    
    def calculate_all_planets(self, dt: datetime, planets: List[str] = None) -> Dict[str, dict]:
        """
        Calculate positions for multiple planets
        
        Args:
            dt: datetime object (UTC)
            planets: List of planet names (defaults to Sun, Moon, Mercury, Venus, Mars)
            
        Returns:
            Dictionary mapping planet names to their data:
            {
                'Sun': {'longitude': 120.5, 'sign': 'Leo', 'degree': 0.5},
                'Moon': {...},
                ...
            }
            
        Raises:
            ValueError: If calculation fails
        """
        if planets is None:
            planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars']
        
        julian_day = self.adapter.datetime_to_julian(dt)
        
        results = {}
        for planet_name in planets:
            try:
                longitude, latitude = self.adapter.calculate_planet_position(planet_name, julian_day)
                sign, degree = self.longitude_to_sign_and_degree(longitude)
                
                results[planet_name] = {
                    'longitude': longitude,
                    'latitude': latitude,
                    'sign': sign,
                    'degree': degree
                }
            except Exception as e:
                raise ValueError(f"Failed to calculate {planet_name}: {e}")
        
        return results
    
    def __del__(self):
        """Cleanup on destruction"""
        if hasattr(self, 'adapter'):
            self.adapter.close()
