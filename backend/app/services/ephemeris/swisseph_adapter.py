"""Swiss Ephemeris Adapter - Low-level wrapper around pyswisseph"""

import swisseph as swe
from datetime import datetime
from typing import Tuple

class SwissEphemerisAdapter:
    """Wrapper for Swiss Ephemeris library with error handling"""
    
    # Planet constants from swisseph
    PLANETS = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mercury': swe.MERCURY,
        'Venus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN
    }
    
    def __init__(self, ephemeris_path: str = None):
        """Initialize Swiss Ephemeris with optional custom path"""
        if ephemeris_path:
            swe.set_ephe_path(ephemeris_path)
    
    @staticmethod
    def datetime_to_julian(dt: datetime) -> float:
        """
        Convert datetime to Julian Day Number
        
        Args:
            dt: datetime object (UTC)
            
        Returns:
            Julian Day Number as float
            
        Raises:
            ValueError: If datetime is invalid
        """
        try:
            jd = swe.julday(
                dt.year,
                dt.month,
                dt.day,
                dt.hour + dt.minute / 60.0 + dt.second / 3600.0
            )
            return jd
        except Exception as e:
            raise ValueError(f"Failed to convert datetime to Julian Day: {e}")
    
    def calculate_planet_position(self, planet_name: str, julian_day: float) -> Tuple[float, float]:
        """
        Calculate planetary position for given Julian Day
        
        Args:
            planet_name: Name of planet (Sun, Moon, Mercury, Venus, Mars, etc.)
            julian_day: Julian Day Number
            
        Returns:
            Tuple of (longitude in degrees, latitude in degrees)
            
        Raises:
            ValueError: If planet name is invalid or calculation fails
        """
        if planet_name not in self.PLANETS:
            raise ValueError(f"Unknown planet: {planet_name}")
        
        try:
            planet_id = self.PLANETS[planet_name]
            result, ret_flag = swe.calc_ut(julian_day, planet_id)
            
            if ret_flag < 0:
                raise ValueError(f"Swiss Ephemeris calculation error for {planet_name}")
            
            longitude = result[0]  # Ecliptic longitude
            latitude = result[1]   # Ecliptic latitude
            
            return longitude, latitude
            
        except Exception as e:
            raise ValueError(f"Failed to calculate position for {planet_name}: {e}")
    
    def calculate_houses(self, julian_day: float, latitude: float, longitude: float, 
                        house_system: str = 'P') -> Tuple[list, list]:
        """
        Calculate house cusps and ascendant/MC
        
        Args:
            julian_day: Julian Day Number
            latitude: Geographic latitude in degrees
            longitude: Geographic longitude in degrees
            house_system: House system code ('P' = Placidus, 'K' = Koch, etc.)
            
        Returns:
            Tuple of (house_cusps, ascmc) where:
                - house_cusps: List of 12 house cusp positions
                - ascmc: List containing [Ascendant, MC, ARMC, Vertex, ...]
                
        Raises:
            ValueError: If calculation fails
        """
        try:
            cusps, ascmc = swe.houses(julian_day, latitude, longitude, house_system.encode())
            return list(cusps), list(ascmc)
        except Exception as e:
            raise ValueError(f"Failed to calculate houses: {e}")
    
    def close(self):
        """Clean up Swiss Ephemeris resources"""
        swe.close()
