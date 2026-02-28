"""
Example usage of Compatibility Aggregator
Demonstrates Mode 1 (single), Mode 2/3 (comparison)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.chart.birth_chart import BirthChartCalculator
from services.aspects.aspect_detector import AspectDetector
from services.aspects.aspect_scorer import AspectScorer
from services.vector.feature_vector_builder import FeatureVectorBuilder
from services.vector.similarity_engine import SimilarityEngine
from services.compatibility.compatibility_aggregator import CompatibilityAggregator

def mode_1_single_person():
    """Mode 1: Single-person love reading (no comparison)"""
    print("=" * 60)
    print("MODE 1: SINGLE-PERSON LOVE READING")
    print("=" * 60)
    
    # Calculate chart
    calculator = BirthChartCalculator()
    chart = calculator.calculate_chart_json(
        date='1990-01-15',
        time='14:30',
        latitude=40.7128,
        longitude=-74.0060
    )
    
    # Build vector
    detector = AspectDetector()
    scorer = AspectScorer()
    planets = {p['name']: p['longitude'] for p in chart['data']['planets']}
    aspects = detector.detect_aspects(planets)
    scores = scorer.score_aspect_list(aspects)
    
    builder = FeatureVectorBuilder()
    vector_data = builder.build_vector(
        chart['data'],
        {'aspects': [a.to_dict() for a in aspects], 'scores': scores}
    )
    
    # Interpret single chart
    aggregator = CompatibilityAggregator()
    profile = aggregator.interpret_single_chart(vector_data['feature_dict'])
    
    print("\n✓ Love Personality Profile:")
    print(f"  Love Readiness:       {profile['love_readiness']:.1f}%")
    print(f"  Emotional Maturity:   {profile['emotional_maturity']:.1f}%")
    print(f"  Relationship Focus:   {profile['relationship_focus']:.1f}%")
    print(f"  Passion Level:        {profile['passion_level']:.1f}%")
    print(f"  Stability Potential:  {profile['stability_potential']:.1f}%")

def mode_2_3_comparison():
    """Mode 2/3: Couple compatibility (with comparison)"""
    print("\n" + "=" * 60)
    print("MODE 2/3: COUPLE COMPATIBILITY")
    print("=" * 60)
    
    # Calculate both charts
    calculator = BirthChartCalculator()
    detector = AspectDetector()
    scorer = AspectScorer()
    builder = FeatureVectorBuilder()
    
    # Person 1
    chart1 = calculator.calculate_chart_json(
        date='1990-01-15',
        time='14:30',
        latitude=40.7128,
        longitude=-74.0060
    )
    
    planets1 = {p['name']: p['longitude'] for p in chart1['data']['planets']}
    aspects1 = detector.detect_aspects(planets1)
    scores1 = scorer.score_aspect_list(aspects1)
    
    vector1_data = builder.build_vector(
        chart1['data'],
        {'aspects': [a.to_dict() for a in aspects1], 'scores': scores1}
    )
    
    # Person 2
    chart2 = calculator.calculate_chart_json(
        date='1992-06-20',
        time='09:15',
        latitude=34.0522,
        longitude=-118.2437
    )
    
    planets2 = {p['name']: p['longitude'] for p in chart2['data']['planets']}
    aspects2 = detector.detect_aspects(planets2)
    scores2 = scorer.score_aspect_list(aspects2)
    
    vector2_data = builder.build_vector(
        chart2['data'],
        {'aspects': [a.to_dict() for a in aspects2], 'scores': scores2}
    )
    
    # Calculate similarity
    similarity_engine = SimilarityEngine()
    similarity_result = similarity_engine.calculate_cosine_similarity(
        vector1_data['feature_vector'],
        vector2_data['feature_vector']
    )
    
    # Aggregate compatibility
    aggregator = CompatibilityAggregator(similarity_weight=0.6, rules_weight=0.4)
    result = aggregator.aggregate_compatibility(
        similarity_result['percentage'],
        vector1_data['feature_dict'],
        vector2_data['feature_dict']
    )
    
    print("\n✓ Compatibility Analysis:")
    print(f"\n  Overall Score:        {result['overall_score']:.1f}%")
    print(f"\n  Components:")
    print(f"    Vector Similarity:  {result['vector_component']:.1f}% (weight: {result['weights']['similarity']})")
    print(f"    Rule-Based Score:   {result['rule_component']:.1f}% (weight: {result['weights']['rules']})")
    print(f"\n  Detailed Indices:")
    print(f"    Emotional Sync:     {result['emotional_sync']:.1f}%")
    print(f"    Chemistry Index:    {result['chemistry_index']:.1f}%")
    print(f"    Stability Index:    {result['stability_index']:.1f}%")

def test_custom_weights():
    """Test with custom weight configuration"""
    print("\n" + "=" * 60)
    print("CUSTOM WEIGHTS TEST")
    print("=" * 60)
    
    # Mock vectors for testing
    vector1 = {
        'venus_element': 0.5, 'mars_element': 1.0, 'moon_stability': 0.6,
        'hard_aspect_density': 0.4, 'soft_aspect_density': 0.6,
        'seventh_house_strength': 0.7, 'venus_mars_harmony': 0.7,
        'sun_moon_balance': 1.0, 'aspect_quality': 0.67,
        'fire_score': 0.5, 'earth_score': 0.3, 'air_score': 0.1, 'water_score': 0.1,
        'fixed_score': 0.4
    }
    
    vector2 = {
        'venus_element': 0.5, 'mars_element': 0.75, 'moon_stability': 0.9,
        'hard_aspect_density': 0.2, 'soft_aspect_density': 0.8,
        'seventh_house_strength': 0.3, 'venus_mars_harmony': 0.7,
        'sun_moon_balance': 0.7, 'aspect_quality': 0.75,
        'fire_score': 0.3, 'earth_score': 0.4, 'air_score': 0.2, 'water_score': 0.1,
        'fixed_score': 0.5
    }
    
    similarity_score = 85.0
    
    # Test different weight configurations
    configs = [
        (0.6, 0.4, "Balanced (default)"),
        (0.8, 0.2, "Vector-heavy"),
        (0.4, 0.6, "Rules-heavy"),
        (0.5, 0.5, "Equal weights")
    ]
    
    print("\nSame data, different weights:\n")
    for sim_w, rule_w, label in configs:
        aggregator = CompatibilityAggregator(sim_w, rule_w)
        result = aggregator.aggregate_compatibility(similarity_score, vector1, vector2)
        print(f"  {label:20s} → Overall: {result['overall_score']:.1f}%")

def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Love Debugging Lab v2.0 - Compatibility Aggregator")
    print("=" * 60)
    print()
    
    try:
        mode_1_single_person()
        mode_2_3_comparison()
        test_custom_weights()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
