"""Birth Chart Calculator - Main orchestration module"""

from datetime import datetime
from typing import Dict, Any
import logging
from ..ephemeris.planetary_calc import PlanetaryCalculator
from .house_system import HouseCalculator
from ...utils.timezone_converter import TimezoneConverter

logger = logging.getLogger(__name__)

class BirthChartCalculator:
    """
    Main birth chart calculation engine
    Orchestrates planetary positions and house calculations
    """
    
    def __init__(self, ephemeris_path: str = None):
        self.planetary_calc = PlanetaryCalculator(ephemeris_path)
        self.house_calc = HouseCalculator(ephemeris_path)
        self.tz_converter = TimezoneConverter()
    
    def calculate_chart(self, date: str, time: str, latitude: float, 
                       longitude: float, timezone: str = 'UTC') -> Dict[str, Any]:
        """
        Calculate complete birth chart
        
        Args:
            date: Birth date in format 'YYYY-MM-DD'
            time: Birth time in format 'HH:MM:SS' or 'HH:MM'
            latitude: Geographic latitude in degrees (-90 to 90)
            longitude: Geographic longitude in degrees (-180 to 180)
            timezone: IANA timezone string (default: 'UTC')
            
        Returns:
            Dictionary containing planets and houses data
            
        Raises:
            ValueError: If input data is invalid or calculation fails
        """
        # Validate inputs
        self._validate_inputs(date, time, latitude, longitude)
        
        # Validate and sanitize timezone
        safe_timezone = self.tz_converter.get_safe_timezone(timezone)
        
        # Convert to UTC for Swiss Ephemeris
        utc_dt = self.tz_converter.convert_to_utc(date, time, safe_timezone)
        
        logger.info(f"Calculating chart for {date} {time} {safe_timezone} (UTC: {utc_dt})")
        
        # Calculate planetary positions (using UTC)
        planets_data = self.planetary_calc.calculate_all_planets(
            utc_dt, 
            planets=['Sun', 'Moon', 'Mercury', 'Venus', 'Mars']
        )
        
        # Calculate houses (using UTC)
        houses_data = self.house_calc.calculate_houses(utc_dt, latitude, longitude)
        
        # Determine house placement for each planet
        for planet_name, planet_info in planets_data.items():
            house_num = HouseCalculator.determine_house_for_planet(
                planet_info['longitude'],
                houses_data['cusps']
            )
            planet_info['house'] = house_num
        
        return {
            'planets': planets_data,
            'houses': houses_data,
            'birth_data': {
                'date': date,
                'time': time,
                'latitude': latitude,
                'longitude': longitude,
                'timezone': safe_timezone,
                'utc_time': utc_dt.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
    
    @staticmethod
    def _validate_inputs(date: str, time: str, latitude: float, longitude: float):
        """Validate input parameters"""
        if not (-90 <= latitude <= 90):
            raise ValueError(f"Invalid latitude: {latitude}. Must be between -90 and 90")
        
        if not (-180 <= longitude <= 180):
            raise ValueError(f"Invalid longitude: {longitude}. Must be between -180 and 180")
        
        # Basic format validation
        if not date or len(date.split('-')) != 3:
            raise ValueError(f"Invalid date format: {date}. Expected YYYY-MM-DD")
        
        if not time or ':' not in time:
            raise ValueError(f"Invalid time format: {time}. Expected HH:MM or HH:MM:SS")
    
    def calculate_chart_json(self, date: str, time: str, latitude: float, 
                            longitude: float, timezone: str = 'UTC') -> dict:
        """
        Calculate chart and return clean JSON-serializable output
        
        Returns structured JSON suitable for API responses
        """
        try:
            chart_data = self.calculate_chart(date, time, latitude, longitude, timezone)
            
            # Format for clean JSON output
            return {
                'success': True,
                'data': {
                    'planets': [
                        {
                            'name': name,
                            'sign': info['sign'],
                            'degree': round(info['degree'], 2),
                            'house': info['house'],
                            'longitude': round(info['longitude'], 2)
                        }
                        for name, info in chart_data['planets'].items()
                    ],
                    'houses': {
                        'system': 'Placidus',
                        'cusps': [round(c, 2) for c in chart_data['houses']['cusps']],
                        'ascendant': {
                            'sign': chart_data['houses']['ascendant_sign'],
                            'degree': round(chart_data['houses']['ascendant_degree'], 2),
                            'longitude': round(chart_data['houses']['ascendant'], 2)
                        },
                        'midheaven': {
                            'sign': chart_data['houses']['mc_sign'],
                            'degree': round(chart_data['houses']['mc_degree'], 2),
                            'longitude': round(chart_data['houses']['mc'], 2)
                        }
                    },
                    'birth_data': chart_data['birth_data']
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
