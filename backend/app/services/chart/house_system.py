"""House System Calculator"""

from datetime import datetime
from typing import List, Tuple
from ..ephemeris.swisseph_adapter import SwissEphemerisAdapter
from ..ephemeris.planetary_calc import PlanetaryCalculator

class HouseCalculator:
    """Calculate astrological houses using various house systems"""
    
    HOUSE_SYSTEMS = {
        'Placidus': 'P',
        'Koch': 'K',
        'Equal': 'E',
        'Whole Sign': 'W'
    }
    
    def __init__(self, ephemeris_path: str = None):
        self.adapter = SwissEphemerisAdapter(ephemeris_path)
    
    def calculate_houses(self, dt: datetime, latitude: float, longitude: float,
                        house_system: str = 'Placidus') -> dict:
        """
        Calculate house cusps and angles
        
        Args:
            dt: datetime object (UTC)
            latitude: Geographic latitude in degrees
            longitude: Geographic longitude in degrees
            house_system: House system name (default: Placidus)
            
        Returns:
            Dictionary containing:
            {
                'cusps': [house1, house2, ..., house12],
                'ascendant': float,
                'mc': float,
                'ascendant_sign': str,
                'mc_sign': str
            }
            
        Raises:
            ValueError: If house system is invalid or calculation fails
        """
        if house_system not in self.HOUSE_SYSTEMS:
            raise ValueError(f"Unknown house system: {house_system}")
        
        system_code = self.HOUSE_SYSTEMS[house_system]
        julian_day = self.adapter.datetime_to_julian(dt)
        
        try:
            cusps, ascmc = self.adapter.calculate_houses(
                julian_day, latitude, longitude, system_code
            )
            
            # ascmc[0] = Ascendant, ascmc[1] = MC
            ascendant = ascmc[0]
            mc = ascmc[1]
            
            asc_sign, asc_degree = PlanetaryCalculator.longitude_to_sign_and_degree(ascendant)
            mc_sign, mc_degree = PlanetaryCalculator.longitude_to_sign_and_degree(mc)
            
            return {
                'cusps': cusps[1:13],  # Houses 1-12 (index 0 is unused)
                'ascendant': ascendant,
                'mc': mc,
                'ascendant_sign': asc_sign,
                'ascendant_degree': asc_degree,
                'mc_sign': mc_sign,
                'mc_degree': mc_degree
            }
            
        except Exception as e:
            raise ValueError(f"House calculation failed: {e}")
    
    @staticmethod
    def determine_house_for_planet(planet_longitude: float, house_cusps: List[float]) -> int:
        """
        Determine which house a planet falls in
        
        Args:
            planet_longitude: Planet's ecliptic longitude (0-360)
            house_cusps: List of 12 house cusp positions
            
        Returns:
            House number (1-12)
        """
        if len(house_cusps) < 12:
            return 1  # Default if insufficient data
        
        planet_longitude = planet_longitude % 360
        
        for i in range(12):
            cusp_start = house_cusps[i] % 360
            # Next cusp wraps to first cusp after 12th house
            cusp_end = house_cusps[0] % 360 if i == 11 else house_cusps[i + 1] % 360
            
            # Handle wrap-around at 0/360 degrees
            if cusp_start < cusp_end:
                if cusp_start <= planet_longitude < cusp_end:
                    return i + 1
            else:  # Wraps around 0 degrees
                if planet_longitude >= cusp_start or planet_longitude < cusp_end:
                    return i + 1
        
        return 1  # Default to 1st house if calculation fails
    
    def __del__(self):
        """Cleanup on destruction"""
        if hasattr(self, 'adapter'):
            self.adapter.close()
