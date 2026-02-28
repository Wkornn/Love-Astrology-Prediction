"""Birth Chart Calculator - Main orchestration module"""

from datetime import datetime
from typing import Dict, Any
from ..ephemeris.planetary_calc import PlanetaryCalculator
from .house_system import HouseCalculator

class BirthChartCalculator:
    """
    Main birth chart calculation engine
    Orchestrates planetary positions and house calculations
    """
    
    def __init__(self, ephemeris_path: str = None):
        self.planetary_calc = PlanetaryCalculator(ephemeris_path)
        self.house_calc = HouseCalculator(ephemeris_path)
    
    def calculate_chart(self, date: str, time: str, latitude: float, 
                       longitude: float, timezone: str = 'UTC') -> Dict[str, Any]:
        """
        Calculate complete birth chart
        
        Args:
            date: Birth date in format 'YYYY-MM-DD'
            time: Birth time in format 'HH:MM:SS' or 'HH:MM'
            latitude: Geographic latitude in degrees (-90 to 90)
            longitude: Geographic longitude in degrees (-180 to 180)
            timezone: Timezone string (default: 'UTC')
            
        Returns:
            Dictionary containing:
            {
                'planets': {
                    'Sun': {'sign': 'Leo', 'degree': 15.5, 'house': 10, 'longitude': 135.5},
                    'Moon': {...},
                    ...
                },
                'houses': {
                    'cusps': [0.0, 30.5, 60.2, ...],
                    'ascendant': 120.5,
                    'ascendant_sign': 'Leo',
                    'mc': 30.2,
                    'mc_sign': 'Taurus'
                }
            }
            
        Raises:
            ValueError: If input data is invalid or calculation fails
        """
        # Validate inputs
        self._validate_inputs(date, time, latitude, longitude)
        
        # Parse datetime
        dt = self._parse_datetime(date, time, timezone)
        
        # Calculate planetary positions
        planets_data = self.planetary_calc.calculate_all_planets(
            dt, 
            planets=['Sun', 'Moon', 'Mercury', 'Venus', 'Mars']
        )
        
        # Calculate houses
        houses_data = self.house_calc.calculate_houses(dt, latitude, longitude)
        
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
                'timezone': timezone
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
    
    @staticmethod
    def _parse_datetime(date: str, time: str, timezone: str) -> datetime:
        """
        Parse date and time strings into datetime object
        
        Note: For simplicity, treating all times as UTC.
        Production version should handle timezone conversion properly.
        """
        try:
            # Handle both HH:MM and HH:MM:SS formats
            if time.count(':') == 1:
                time += ':00'
            
            dt_str = f"{date} {time}"
            dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
            
            return dt
            
        except Exception as e:
            raise ValueError(f"Failed to parse datetime: {e}")
    
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
