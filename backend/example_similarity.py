"""
Example usage of Similarity Engine
Demonstrates cosine similarity calculation between feature vectors
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.chart.birth_chart import BirthChartCalculator
from services.aspects.aspect_detector import AspectDetector
from services.aspects.aspect_scorer import AspectScorer
from services.vector.feature_vector_builder import FeatureVectorBuilder
from services.vector.similarity_engine import SimilarityEngine

def test_basic_similarity():
    """Test basic similarity calculation"""
    print("=" * 60)
    print("TEST 1: Basic Similarity Calculation")
    print("=" * 60)
    
    # Test vectors
    vector_a = [0.5, 1.0, 0.6, 0.4, 0.6, 0.7, 0.7, 1.0, 0.67]
    vector_b = [0.5, 0.75, 0.9, 0.2, 0.8, 0.3, 0.7, 0.7, 0.75]
    
    print(f"\nVector A: {vector_a}")
    print(f"Vector B: {vector_b}")
    
    # Cosine similarity
    result = SimilarityEngine.calculate_cosine_similarity(vector_a, vector_b)
    print(f"\nCosine Similarity:")
    print(f"  Score: {result['similarity_score']}")
    print(f"  Percentage: {result['percentage']}%")
    
    # Euclidean similarity
    result2 = SimilarityEngine.calculate_euclidean_similarity(vector_a, vector_b)
    print(f"\nEuclidean Similarity:")
    print(f"  Score: {result2['similarity_score']}")
    print(f"  Percentage: {result2['percentage']}%")

def test_edge_cases():
    """Test edge cases"""
    print("\n" + "=" * 60)
    print("TEST 2: Edge Cases")
    print("=" * 60)
    
    engine = SimilarityEngine()
    
    # Identical vectors
    identical = [0.5, 0.5, 0.5]
    result = engine.calculate_cosine_similarity(identical, identical)
    print(f"\nIdentical vectors: {result['percentage']}%")
    assert result['similarity_score'] == 1.0, "Identical vectors should have 100% similarity"
    
    # Orthogonal vectors
    orthogonal_a = [1.0, 0.0, 0.0]
    orthogonal_b = [0.0, 1.0, 0.0]
    result = engine.calculate_cosine_similarity(orthogonal_a, orthogonal_b)
    print(f"Orthogonal vectors: {result['percentage']}%")
    
    # Zero vector handling
    try:
        zero_vector = [0.0, 0.0, 0.0]
        normal_vector = [1.0, 1.0, 1.0]
        result = engine.calculate_cosine_similarity(zero_vector, normal_vector)
        print(f"Zero vector: {result['percentage']}%")
        assert result['similarity_score'] == 0.0, "Zero vector should return 0% similarity"
    except Exception as e:
        print(f"Zero vector error: {e}")
    
    # Different length vectors
    try:
        short = [1.0, 2.0]
        long = [1.0, 2.0, 3.0]
        engine.calculate_cosine_similarity(short, long)
        print("ERROR: Should have raised ValueError for different lengths")
    except ValueError as e:
        print(f"Different lengths correctly rejected: {e}")

def test_real_charts():
    """Test with real birth chart data"""
    print("\n" + "=" * 60)
    print("TEST 3: Real Birth Chart Comparison")
    print("=" * 60)
    
    try:
        # Calculate two charts
        calculator = BirthChartCalculator()
        detector = AspectDetector()
        scorer = AspectScorer()
        builder = FeatureVectorBuilder()
        engine = SimilarityEngine()
        
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
        
        # Compare
        print("\nPerson 1: Born 1990-01-15, New York")
        print("Person 2: Born 1992-06-20, Los Angeles")
        
        result = engine.compare_vectors(
            vector1_data['feature_vector'],
            vector2_data['feature_vector'],
            method='cosine'
        )
        
        print(f"\nCompatibility Analysis:")
        print(f"  Method: {result['method']}")
        print(f"  Similarity Score: {result['similarity_score']}")
        print(f"  Percentage: {result['percentage']}%")
        print(f"  Interpretation: {result['interpretation']}")
        
        # Show feature comparison
        print(f"\nFeature Breakdown:")
        for i, label in enumerate(vector1_data['feature_labels']):
            v1 = vector1_data['feature_vector'][i]
            v2 = vector2_data['feature_vector'][i]
            diff = abs(v1 - v2)
            match = "✓" if diff < 0.2 else "✗"
            print(f"  {match} {label:25s} {v1:.3f} vs {v2:.3f} (diff: {diff:.3f})")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Love Debugging Lab v2.0 - Similarity Engine")
    print("=" * 60)
    print()
    
    test_basic_similarity()
    test_edge_cases()
    test_real_charts()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == '__main__':
    main()
