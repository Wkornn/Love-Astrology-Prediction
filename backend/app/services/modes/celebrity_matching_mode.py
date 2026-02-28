"""Mode 2: Celebrity Matching Mode"""

from typing import Dict, Any, List
from .mode_interface import ModeInterface
from ..chart.birth_chart import BirthChartCalculator
from ..vector.vector_builder import ChartVectorBuilder
import json
import os

class CelebrityMatchingMode(ModeInterface):
    """
    Mode 2: Celebrity matching
    Compare user's chart against pre-stored celebrity database
    """
    
    def __init__(self, celebrity_db_path: str = None):
        self.chart_calculator = BirthChartCalculator()
        self.vector_builder = ChartVectorBuilder()
        self.celebrity_db_path = celebrity_db_path or self._get_default_db_path()
        self.celebrity_db = self._load_celebrity_db()
    
    @property
    def mode_name(self) -> str:
        return "celebrity_matching"
    
    def _get_default_db_path(self) -> str:
        """Get default celebrity database path"""
        return os.path.join(
            os.path.dirname(__file__), 
            '../../data/celebrities.json'
        )
    
    def _load_celebrity_db(self) -> List[Dict]:
        """Load celebrity database"""
        if os.path.exists(self.celebrity_db_path):
            with open(self.celebrity_db_path, 'r') as f:
                return json.load(f)
        return []
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate celebrity matching input"""
        required = ['date', 'time', 'latitude', 'longitude']
        for field in required:
            if field not in input_data:
                raise ValueError(f"Missing required field: {field}")
        return True
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute celebrity matching
        
        Input:
            {
                'date': 'YYYY-MM-DD',
                'time': 'HH:MM',
                'latitude': float,
                'longitude': float,
                'timezone': 'UTC' (optional),
                'top_n': 5 (optional)
            }
        
        Output:
            {
                'mode': 'celebrity_matching',
                'user_vector': {...},
                'matches': [
                    {
                        'name': 'Celebrity Name',
                        'similarity_score': 85.5,
                        'match_reason': '...'
                    }
                ]
            }
        """
        self.validate_input(input_data)
        
        # Calculate user's chart
        chart_json = self.chart_calculator.calculate_chart_json(
            date=input_data['date'],
            time=input_data['time'],
            latitude=input_data['latitude'],
            longitude=input_data['longitude'],
            timezone=input_data.get('timezone', 'UTC')
        )
        
        if not chart_json['success']:
            raise ValueError(f"Chart calculation failed: {chart_json.get('error')}")
        
        # Build user vector
        user_vector = self.vector_builder.build_vector(chart_json['data'])
        
        # Compare with celebrities
        matches = self._find_matches(user_vector, input_data.get('top_n', 5))
        
        return {
            'mode': self.mode_name,
            'user_vector': user_vector,
            'matches': matches,
            'total_celebrities': len(self.celebrity_db)
        }
    
    def _find_matches(self, user_vector: Dict[str, float], top_n: int) -> List[Dict]:
        """Find top N celebrity matches"""
        
        if not self.celebrity_db:
            return [{
                'name': 'Sample Celebrity',
                'similarity_score': 75.0,
                'match_reason': 'Database not loaded - this is a demo result'
            }]
        
        matches = []
        
        for celebrity in self.celebrity_db:
            if 'vector' not in celebrity:
                continue
            
            similarity = self.vector_builder.calculate_similarity(
                user_vector, 
                celebrity['vector']
            )
            
            matches.append({
                'name': celebrity['name'],
                'similarity_score': similarity,
                'match_reason': self._generate_match_reason(user_vector, celebrity['vector'])
            })
        
        # Sort by similarity and return top N
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        return matches[:top_n]
    
    def _generate_match_reason(self, user_vector: Dict[str, float], 
                               celeb_vector: Dict[str, float]) -> str:
        """Generate explanation for match"""
        
        # Find strongest similarity
        similarities = {}
        for key in user_vector:
            if key in celeb_vector:
                diff = abs(user_vector[key] - celeb_vector[key])
                similarities[key] = 1.0 - diff
        
        strongest = max(similarities, key=similarities.get)
        
        reasons = {
            'fire_score': 'Similar passionate energy',
            'earth_score': 'Shared practical approach',
            'air_score': 'Compatible communication styles',
            'water_score': 'Matching emotional depth',
            'venus_mars_harmony': 'Aligned romantic expression',
            'sun_moon_balance': 'Similar emotional balance'
        }
        
        return reasons.get(strongest, 'Compatible astrological profile')
