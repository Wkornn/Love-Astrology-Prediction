"""Import celebrities to database from JSON file"""

import json
import sys
sys.path.insert(0, 'backend')

from app.database.public_figure_db import PublicFigureDatabase
from app.services.chart.birth_chart import BirthChartCalculator
from app.services.vector.feature_vector_builder import FeatureVectorBuilder

def import_to_db():
    """Import celebrities from JSON file"""
    
    # Read geocoded data
    with open('celebs_with_coords.json', 'r', encoding='utf-8') as f:
        celebs = json.load(f)
    
    print(f"🌟 Importing {len(celebs)} celebrities to database...\n")
    
    db = PublicFigureDatabase()
    chart_calc = BirthChartCalculator()
    vector_builder = FeatureVectorBuilder()
    
    imported = 0
    failed = []
    
    for celeb in celebs:
        print(f"📍 {celeb['name']}")
        
        try:
            # Calculate birth chart
            chart = chart_calc.calculate_chart(
                celeb['birth_date'],
                celeb['birth_time'],
                celeb['latitude'],
                celeb['longitude'],
                celeb['timezone']
            )
            
            # Debug: print chart type
            if not isinstance(chart, dict):
                raise ValueError(f"Chart is not dict, got: {type(chart)}")
            
            if 'planets' not in chart or 'houses' not in chart:
                raise ValueError(f"Chart missing keys. Has: {list(chart.keys())}")
            
            # Convert planets dict to list format expected by build_vector
            planets_list = [
                {'name': name, **data} 
                for name, data in chart['planets'].items()
            ]
            
            chart_for_vector = {
                'planets': planets_list,
                'houses': chart['houses']
            }
            
            # Build feature vector
            vector_result = vector_builder.build_vector(chart_for_vector)
            
            # Debug: check vector_result type
            if isinstance(vector_result, dict) and 'feature_vector' in vector_result:
                feature_vector = vector_result['feature_vector']
            elif isinstance(vector_result, list):
                feature_vector = vector_result
            else:
                raise ValueError(f"Unexpected vector format: {type(vector_result)}")
            
            # Add to database
            figure_id = db.add_figure(
                name=celeb['name'],
                birth_date=celeb['birth_date'],
                latitude=celeb['latitude'],
                longitude=celeb['longitude'],
                birth_time=celeb['birth_time'],
                timezone=celeb['timezone'],
                occupation=celeb.get('category', None),
                feature_vector=feature_vector
            )
            
            print(f"   ✅ Imported (ID: {figure_id})")
            imported += 1
            
        except Exception as e:
            import traceback
            print(f"   ❌ Error: {e}")
            print(f"   Debug: {traceback.format_exc()[:200]}")
            failed.append(celeb['name'])
    
    print(f"\n{'='*50}")
    print(f"✅ Successfully imported: {imported}/{len(celebs)}")
    
    if failed:
        print(f"\n❌ Failed ({len(failed)}):")
        for name in failed:
            print(f"   - {name}")
    
    # Show stats
    stats = db.get_stats()
    print(f"\n📊 Database Stats:")
    print(f"   Total figures: {stats['total_figures']}")
    print(f"   Cached vectors: {stats['cached_vectors']}")

if __name__ == '__main__':
    import_to_db()
