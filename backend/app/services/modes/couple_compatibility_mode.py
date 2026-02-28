"""Mode 3: Couple Compatibility Mode"""

from typing import Dict, Any
from .mode_interface import ModeInterface
from ..chart.birth_chart import BirthChartCalculator
from ..vector.vector_builder import ChartVectorBuilder

class CoupleCompatibilityMode(ModeInterface):
    """
    Mode 3: Couple compatibility analysis
    Compare two users' charts for similarity score
    """
    
    def __init__(self):
        self.chart_calculator = BirthChartCalculator()
        self.vector_builder = ChartVectorBuilder()
    
    @property
    def mode_name(self) -> str:
        return "couple_compatibility"
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate couple compatibility input"""
        if 'person1' not in input_data or 'person2' not in input_data:
            raise ValueError("Both person1 and person2 data required")
        
        for person in ['person1', 'person2']:
            required = ['date', 'time', 'latitude', 'longitude']
            for field in required:
                if field not in input_data[person]:
                    raise ValueError(f"Missing {field} for {person}")
        
        return True
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute couple compatibility analysis
        
        Input:
            {
                'person1': {
                    'date': 'YYYY-MM-DD',
                    'time': 'HH:MM',
                    'latitude': float,
                    'longitude': float,
                    'timezone': 'UTC' (optional)
                },
                'person2': {
                    'date': 'YYYY-MM-DD',
                    'time': 'HH:MM',
                    'latitude': float,
                    'longitude': float,
                    'timezone': 'UTC' (optional)
                }
            }
        
        Output:
            {
                'mode': 'couple_compatibility',
                'person1_vector': {...},
                'person2_vector': {...},
                'similarity_score': 85.5,
                'compatibility_breakdown': {...},
                'strengths': [...],
                'challenges': [...]
            }
        """
        self.validate_input(input_data)
        
        # Calculate both charts
        chart1_json = self._calculate_chart(input_data['person1'])
        chart2_json = self._calculate_chart(input_data['person2'])
        
        # Build vectors
        vector1 = self.vector_builder.build_vector(chart1_json['data'])
        vector2 = self.vector_builder.build_vector(chart2_json['data'])
        
        # Calculate similarity
        similarity_score = self.vector_builder.calculate_similarity(vector1, vector2)
        
        # Detailed breakdown
        breakdown = self._calculate_breakdown(vector1, vector2)
        strengths, challenges = self._analyze_compatibility(vector1, vector2, breakdown)
        
        return {
            'mode': self.mode_name,
            'person1_vector': vector1,
            'person2_vector': vector2,
            'similarity_score': similarity_score,
            'compatibility_breakdown': breakdown,
            'strengths': strengths,
            'challenges': challenges
        }
    
    def _calculate_chart(self, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate chart for one person"""
        return self.chart_calculator.calculate_chart_json(
            date=person_data['date'],
            time=person_data['time'],
            latitude=person_data['latitude'],
            longitude=person_data['longitude'],
            timezone=person_data.get('timezone', 'UTC')
        )
    
    def _calculate_breakdown(self, vector1: Dict[str, float], 
                            vector2: Dict[str, float]) -> Dict[str, float]:
        """Calculate detailed compatibility breakdown"""
        
        categories = {
            'emotional': ['water_score', 'sun_moon_balance'],
            'physical': ['fire_score', 'venus_mars_harmony'],
            'intellectual': ['air_score'],
            'stability': ['earth_score', 'fixed_score']
        }
        
        breakdown = {}
        
        for category, keys in categories.items():
            scores = []
            for key in keys:
                if key in vector1 and key in vector2:
                    diff = abs(vector1[key] - vector2[key])
                    similarity = (1.0 - diff) * 100
                    scores.append(similarity)
            
            breakdown[category] = round(sum(scores) / len(scores), 2) if scores else 50.0
        
        return breakdown
    
    def _analyze_compatibility(self, vector1: Dict[str, float], 
                               vector2: Dict[str, float],
                               breakdown: Dict[str, float]) -> tuple:
        """Identify strengths and challenges"""
        
        strengths = []
        challenges = []
        
        # Check element compatibility
        for element in ['fire', 'earth', 'air', 'water']:
            key = f'{element}_score'
            diff = abs(vector1[key] - vector2[key])
            
            if diff < 0.2:
                strengths.append(f"Similar {element} energy - natural understanding")
            elif diff > 0.5:
                challenges.append(f"Different {element} expression - requires compromise")
        
        # Venus-Mars harmony
        if abs(vector1['venus_mars_harmony'] - vector2['venus_mars_harmony']) < 0.2:
            strengths.append("Compatible romantic and passionate expression")
        
        # Breakdown analysis
        for category, score in breakdown.items():
            if score > 75:
                strengths.append(f"Strong {category} compatibility")
            elif score < 50:
                challenges.append(f"{category.capitalize()} differences need attention")
        
        return strengths[:3], challenges[:3]  # Top 3 each
