"""
Example usage of Feature Vector Builder
Demonstrates feature extraction from natal chart + aspects
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.chart.birth_chart import BirthChartCalculator
from services.aspects.aspect_detector import AspectDetector
from services.aspects.aspect_scorer import AspectScorer
from services.vector.feature_vector_builder import FeatureVectorBuilder
import json

def main():
    """Test feature vector building"""
    
    print("=" * 60)
    print("Love Debugging Lab v2.0 - Feature Vector Builder")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Calculate birth chart
        print("Step 1: Calculating birth chart...")
        calculator = BirthChartCalculator()
        chart = calculator.calculate_chart_json(
            date='1990-01-15',
            time='14:30',
            latitude=40.7128,
            longitude=-74.0060,
            timezone='UTC'
        )
        
        if not chart['success']:
            print(f"✗ Chart calculation failed: {chart.get('error')}")
            return
        
        print("✓ Chart calculated")
        
        # Step 2: Detect aspects
        print("\nStep 2: Detecting aspects...")
        planets = {
            p['name']: p['longitude'] 
            for p in chart['data']['planets']
        }
        
        detector = AspectDetector()
        aspects = detector.detect_aspects(planets)
        scorer = AspectScorer()
        aspect_scores = scorer.score_aspect_list(aspects)
        
        aspects_data = {
            'aspects': [a.to_dict() for a in aspects],
            'scores': aspect_scores
        }
        
        print(f"✓ Found {len(aspects)} aspects")
        print(f"  Harmonious: {aspect_scores['harmonious_count']}")
        print(f"  Challenging: {aspect_scores['challenging_count']}")
        
        # Step 3: Build feature vector
        print("\nStep 3: Building feature vector...")
        builder = FeatureVectorBuilder()
        result = builder.build_vector(chart['data'], aspects_data)
        
        print(f"✓ Feature vector built ({result['dimensions']} dimensions)")
        
        # Display results
        print("\n" + "=" * 60)
        print("FEATURE VECTOR")
        print("=" * 60)
        
        print("\nFeature Breakdown:")
        for label, value in result['feature_dict'].items():
            bar = "█" * int(value * 20)
            print(f"  {label:25s} {value:.3f} {bar}")
        
        print(f"\nRaw Vector: {result['feature_vector']}")
        print(f"Labels: {result['feature_labels']}")
        
        # Test similarity calculation
        print("\n" + "=" * 60)
        print("SIMILARITY TEST")
        print("=" * 60)
        
        # Calculate another chart for comparison
        chart2 = calculator.calculate_chart_json(
            date='1992-06-20',
            time='09:15',
            latitude=34.0522,
            longitude=-118.2437,
            timezone='UTC'
        )
        
        if chart2['success']:
            planets2 = {
                p['name']: p['longitude'] 
                for p in chart2['data']['planets']
            }
            aspects2 = detector.detect_aspects(planets2)
            scores2 = scorer.score_aspect_list(aspects2)
            
            aspects_data2 = {
                'aspects': [a.to_dict() for a in aspects2],
                'scores': scores2
            }
            
            result2 = builder.build_vector(chart2['data'], aspects_data2)
            
            similarity = builder.calculate_similarity(
                result['feature_vector'],
                result2['feature_vector']
            )
            
            print(f"\nChart 1 vs Chart 2 Similarity: {similarity}%")
            
            # Show feature differences
            print("\nFeature Comparison:")
            for i, label in enumerate(result['feature_labels']):
                v1 = result['feature_vector'][i]
                v2 = result2['feature_vector'][i]
                diff = abs(v1 - v2)
                print(f"  {label:25s} {v1:.3f} vs {v2:.3f} (diff: {diff:.3f})")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
