"""
Example usage of Public Figure Database
Demonstrates CRUD operations, caching, and matching
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from database.public_figure_db import PublicFigureDatabase
from services.chart.birth_chart import BirthChartCalculator
from services.aspects.aspect_detector import AspectDetector
from services.aspects.aspect_scorer import AspectScorer
from services.vector.feature_vector_builder import FeatureVectorBuilder
from services.vector.similarity_engine import SimilarityEngine
import json

def setup_database():
    """Initialize database and import sample data"""
    print("=" * 60)
    print("SETUP: Initialize Database")
    print("=" * 60)
    
    db = PublicFigureDatabase()
    
    # Load sample figures
    sample_path = os.path.join(
        os.path.dirname(__file__),
        'app/data/sample_figures.json'
    )
    
    if os.path.exists(sample_path):
        with open(sample_path, 'r') as f:
            figures = json.load(f)
        
        imported = db.bulk_import(figures)
        print(f"\n✓ Imported {imported} figures")
    else:
        print("\n⚠ Sample data file not found, adding manual entries...")
        
        # Add a few manually
        try:
            db.add_figure(
                name="Sample Celebrity A",
                birth_date="1990-05-15",
                birth_time="14:30",
                latitude=40.7128,
                longitude=-74.0060,
                occupation="Actor"
            )
            print("✓ Added Sample Celebrity A")
        except ValueError:
            print("⚠ Sample Celebrity A already exists")
    
    stats = db.get_stats()
    print(f"\nDatabase Stats:")
    print(f"  Total Figures: {stats['total_figures']}")
    print(f"  Cached Vectors: {stats['cached_vectors']}")
    print(f"  Cache Coverage: {stats['cache_percentage']}%")

def compute_and_cache_vectors():
    """Compute feature vectors for all figures without cached vectors"""
    print("\n" + "=" * 60)
    print("COMPUTE: Calculate and Cache Vectors")
    print("=" * 60)
    
    db = PublicFigureDatabase()
    calculator = BirthChartCalculator()
    detector = AspectDetector()
    scorer = AspectScorer()
    builder = FeatureVectorBuilder()
    
    figures = db.get_all_figures(include_vectors=True)
    
    computed = 0
    for figure in figures:
        # Skip if already cached
        if figure.get('feature_vector'):
            print(f"⊙ {figure['name']:30s} [cached]")
            continue
        
        # Skip if no birth time
        if not figure['birth_time']:
            print(f"⊘ {figure['name']:30s} [no birth time]")
            continue
        
        try:
            # Calculate chart
            chart = calculator.calculate_chart_json(
                date=figure['birth_date'],
                time=figure['birth_time'],
                latitude=figure['birth_latitude'],
                longitude=figure['birth_longitude'],
                timezone=figure.get('birth_timezone', 'UTC')
            )
            
            if not chart['success']:
                print(f"✗ {figure['name']:30s} [chart failed]")
                continue
            
            # Detect aspects
            planets = {p['name']: p['longitude'] for p in chart['data']['planets']}
            aspects = detector.detect_aspects(planets)
            scores = scorer.score_aspect_list(aspects)
            
            # Build vector
            vector_data = builder.build_vector(
                chart['data'],
                {'aspects': [a.to_dict() for a in aspects], 'scores': scores}
            )
            
            # Cache vector
            db.cache_vector(figure['id'], vector_data['feature_vector'])
            
            print(f"✓ {figure['name']:30s} [computed & cached]")
            computed += 1
            
        except Exception as e:
            print(f"✗ {figure['name']:30s} [error: {e}]")
    
    print(f"\n✓ Computed {computed} new vectors")

def test_queries():
    """Test database query operations"""
    print("\n" + "=" * 60)
    print("TEST: Query Operations")
    print("=" * 60)
    
    db = PublicFigureDatabase()
    
    # Get all figures
    all_figures = db.get_all_figures()
    print(f"\n✓ Total figures: {len(all_figures)}")
    
    # Find by exact name
    if all_figures:
        first_name = all_figures[0]['name']
        figure = db.find_by_name(first_name)
        if figure:
            print(f"\n✓ Found by exact name: {figure['name']}")
            print(f"  Born: {figure['birth_date']} at {figure['birth_time'] or 'unknown time'}")
            print(f"  Location: ({figure['birth_latitude']}, {figure['birth_longitude']})")
            print(f"  Vector cached: {'Yes' if figure.get('feature_vector') else 'No'}")
    
    # Fuzzy search
    fuzzy_result = db.find_by_name("Taylor", fuzzy=True)
    if fuzzy_result:
        print(f"\n✓ Fuzzy search 'Taylor': {fuzzy_result['name']}")

def test_matching():
    """Test user-to-celebrity matching"""
    print("\n" + "=" * 60)
    print("TEST: Celebrity Matching")
    print("=" * 60)
    
    db = PublicFigureDatabase()
    calculator = BirthChartCalculator()
    detector = AspectDetector()
    scorer = AspectScorer()
    builder = FeatureVectorBuilder()
    engine = SimilarityEngine()
    
    # Calculate user chart
    print("\nCalculating user chart...")
    user_chart = calculator.calculate_chart_json(
        date='1995-03-20',
        time='15:30',
        latitude=40.7128,
        longitude=-74.0060
    )
    
    if not user_chart['success']:
        print("✗ User chart calculation failed")
        return
    
    # Build user vector
    planets = {p['name']: p['longitude'] for p in user_chart['data']['planets']}
    aspects = detector.detect_aspects(planets)
    scores = scorer.score_aspect_list(aspects)
    
    user_vector_data = builder.build_vector(
        user_chart['data'],
        {'aspects': [a.to_dict() for a in aspects], 'scores': scores}
    )
    
    print("✓ User vector computed")
    
    # Match against all celebrities
    def similarity_func(vec1, vec2):
        result = engine.calculate_cosine_similarity(vec1, vec2)
        return result['percentage']
    
    matches = db.match_user_to_all(
        user_vector_data['feature_vector'],
        similarity_func,
        top_n=5
    )
    
    if matches:
        print(f"\n✓ Top {len(matches)} Celebrity Matches:")
        for i, (figure, score) in enumerate(matches, 1):
            print(f"\n  {i}. {figure['name']}")
            print(f"     Similarity: {score:.1f}%")
            print(f"     Occupation: {figure.get('occupation', 'Unknown')}")
    else:
        print("\n⚠ No matches found (no cached vectors)")

def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Love Debugging Lab v2.0 - Public Figure Database")
    print("=" * 60)
    print()
    
    try:
        setup_database()
        compute_and_cache_vectors()
        test_queries()
        test_matching()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
