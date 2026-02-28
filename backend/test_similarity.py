"""Unit tests for Similarity Engine"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.vector.similarity_engine import SimilarityEngine
import math

def test_identical_vectors():
    """Test that identical vectors return 100% similarity"""
    vector = [0.5, 0.7, 0.3, 0.9]
    result = SimilarityEngine.calculate_cosine_similarity(vector, vector)
    
    assert result['similarity_score'] == 1.0, "Identical vectors should have score 1.0"
    assert result['percentage'] == 100.0, "Identical vectors should have 100%"
    print("✓ test_identical_vectors passed")

def test_orthogonal_vectors():
    """Test orthogonal vectors (should be 0% similar)"""
    vector_a = [1.0, 0.0, 0.0]
    vector_b = [0.0, 1.0, 0.0]
    result = SimilarityEngine.calculate_cosine_similarity(vector_a, vector_b)
    
    assert result['similarity_score'] == 0.0, "Orthogonal vectors should have score 0.0"
    assert result['percentage'] == 0.0, "Orthogonal vectors should have 0%"
    print("✓ test_orthogonal_vectors passed")

def test_zero_vector():
    """Test zero vector handling"""
    zero = [0.0, 0.0, 0.0]
    normal = [1.0, 1.0, 1.0]
    result = SimilarityEngine.calculate_cosine_similarity(zero, normal)
    
    assert result['similarity_score'] == 0.0, "Zero vector should return 0.0"
    assert result['percentage'] == 0.0, "Zero vector should return 0%"
    print("✓ test_zero_vector passed")

def test_opposite_vectors():
    """Test opposite direction vectors"""
    vector_a = [1.0, 1.0, 1.0]
    vector_b = [-1.0, -1.0, -1.0]
    result = SimilarityEngine.calculate_cosine_similarity(vector_a, vector_b)
    
    # Cosine of 180° = -1, but we clamp to [0, 1]
    assert result['similarity_score'] == 0.0, "Opposite vectors should have score 0.0"
    print("✓ test_opposite_vectors passed")

def test_different_lengths():
    """Test that different length vectors raise error"""
    vector_a = [1.0, 2.0]
    vector_b = [1.0, 2.0, 3.0]
    
    try:
        SimilarityEngine.calculate_cosine_similarity(vector_a, vector_b)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "length mismatch" in str(e).lower()
        print("✓ test_different_lengths passed")

def test_empty_vectors():
    """Test that empty vectors raise error"""
    try:
        SimilarityEngine.calculate_cosine_similarity([], [])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()
        print("✓ test_empty_vectors passed")

def test_known_similarity():
    """Test with known similarity value"""
    # Two vectors at 60° angle should have cosine similarity = 0.5
    vector_a = [1.0, 0.0]
    vector_b = [0.5, math.sqrt(3)/2]  # 60° from vector_a
    
    result = SimilarityEngine.calculate_cosine_similarity(vector_a, vector_b)
    
    # Allow small floating point error
    assert abs(result['similarity_score'] - 0.5) < 0.01, f"Expected ~0.5, got {result['similarity_score']}"
    print("✓ test_known_similarity passed")

def test_euclidean_similarity():
    """Test Euclidean similarity calculation"""
    vector_a = [0.5, 0.5, 0.5]
    vector_b = [0.5, 0.5, 0.5]
    
    result = SimilarityEngine.calculate_euclidean_similarity(vector_a, vector_b)
    
    assert result['similarity_score'] == 1.0, "Identical vectors should have score 1.0"
    assert result['percentage'] == 100.0, "Identical vectors should have 100%"
    print("✓ test_euclidean_similarity passed")

def test_compare_vectors():
    """Test compare_vectors method"""
    vector_a = [0.8, 0.7, 0.9]
    vector_b = [0.75, 0.65, 0.85]
    
    result = SimilarityEngine.compare_vectors(vector_a, vector_b, method='cosine')
    
    assert 'method' in result
    assert 'similarity_score' in result
    assert 'percentage' in result
    assert 'interpretation' in result
    assert result['method'] == 'cosine'
    print("✓ test_compare_vectors passed")

def test_interpretation_levels():
    """Test interpretation categorization"""
    engine = SimilarityEngine()
    
    # High similarity
    high = [0.9, 0.9, 0.9]
    result = engine.compare_vectors(high, high, method='cosine')
    assert 'high' in result['interpretation'].lower()
    
    # Low similarity
    low_a = [1.0, 0.0, 0.0]
    low_b = [0.0, 0.0, 1.0]
    result = engine.compare_vectors(low_a, low_b, method='cosine')
    assert 'low' in result['interpretation'].lower()
    
    print("✓ test_interpretation_levels passed")

def run_all_tests():
    """Run all unit tests"""
    print("=" * 60)
    print("Running Similarity Engine Unit Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_identical_vectors,
        test_orthogonal_vectors,
        test_zero_vector,
        test_opposite_vectors,
        test_different_lengths,
        test_empty_vectors,
        test_known_similarity,
        test_euclidean_similarity,
        test_compare_vectors,
        test_interpretation_levels
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
