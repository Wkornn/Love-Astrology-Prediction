"""Mode 1: Single-Person Love Reading"""

from typing import Dict, Any
from .mode_interface import ModeInterface
from ..chart.birth_chart import BirthChartCalculator
from ..aspects.aspect_detector import AspectDetector
from ..aspects.aspect_scorer import AspectScorer
from ..vector.vector_builder import ChartVectorBuilder

class SinglePersonMode(ModeInterface):
    """
    Mode 1: Single-person love personality analysis
    Analyzes one person's natal chart for love traits
    """
    
    def __init__(self):
        self.chart_calculator = BirthChartCalculator()
        self.aspect_detector = AspectDetector()
        self.aspect_scorer = AspectScorer()
        self.vector_builder = ChartVectorBuilder()
    
    @property
    def mode_name(self) -> str:
        return "single_person"
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate single person input"""
        required = ['date', 'time', 'latitude', 'longitude']
        for field in required:
            if field not in input_data:
                raise ValueError(f"Missing required field: {field}")
        return True
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute single-person love reading
        
        Input:
            {
                'date': 'YYYY-MM-DD',
                'time': 'HH:MM',
                'latitude': float,
                'longitude': float,
                'timezone': 'UTC' (optional)
            }
        
        Output:
            {
                'mode': 'single_person',
                'chart': {...},
                'aspects': {...},
                'personality_vector': {...},
                'love_profile': {...}
            }
        """
        self.validate_input(input_data)
        
        # Calculate birth chart
        chart = self.chart_calculator.calculate_chart(
            date=input_data['date'],
            time=input_data['time'],
            latitude=input_data['latitude'],
            longitude=input_data['longitude'],
            timezone=input_data.get('timezone', 'UTC')
        )
        
        # Detect aspects
        planets = {name: info['longitude'] for name, info in chart['planets'].items()}
        aspects = self.aspect_detector.detect_aspects(planets)
        aspect_scores = self.aspect_scorer.score_aspect_list(aspects)
        
        # Build personality vector
        chart_json = self.chart_calculator.calculate_chart_json(
            date=input_data['date'],
            time=input_data['time'],
            latitude=input_data['latitude'],
            longitude=input_data['longitude'],
            timezone=input_data.get('timezone', 'UTC')
        )
        
        personality_vector = self.vector_builder.build_vector(chart_json['data'])
        
        # Generate love profile
        love_profile = self._generate_love_profile(personality_vector, aspect_scores)
        
        return {
            'mode': self.mode_name,
            'chart': chart,
            'aspects': {
                'total': len(aspects),
                'scores': aspect_scores,
                'details': [a.to_dict() for a in aspects[:5]]  # Top 5
            },
            'personality_vector': personality_vector,
            'love_profile': love_profile
        }
    
    def _generate_love_profile(self, vector: Dict[str, float], 
                               aspect_scores: Dict[str, float]) -> Dict[str, Any]:
        """Generate love personality profile"""
        
        # Determine dominant element
        elements = {
            'Fire': vector['fire_score'],
            'Earth': vector['earth_score'],
            'Air': vector['air_score'],
            'Water': vector['water_score']
        }
        dominant_element = max(elements, key=elements.get)
        
        # Love style based on element
        love_styles = {
            'Fire': 'Passionate and spontaneous',
            'Earth': 'Stable and sensual',
            'Air': 'Intellectual and communicative',
            'Water': 'Emotional and intuitive'
        }
        
        # Emotional intensity
        emotional_intensity = (
            vector['water_score'] * 0.5 + 
            vector['fire_score'] * 0.3 + 
            aspect_scores.get('average_strength', 0.5) * 0.2
        )
        
        return {
            'dominant_element': dominant_element,
            'love_style': love_styles[dominant_element],
            'emotional_intensity': round(emotional_intensity, 2),
            'venus_mars_harmony': vector['venus_mars_harmony'],
            'relationship_stability': round(vector['earth_score'] + vector['fixed_score'], 2),
            'communication_style': 'Direct' if vector['fire_score'] > 0.3 else 'Thoughtful'
        }
