"""Similarity Engine - Computes similarity between feature vectors"""

from typing import List, Dict, Union
import math

class SimilarityEngine:
    """
    Computes similarity between feature vectors using cosine similarity
    
    Formula: similarity = dot(A, B) / (||A|| * ||B||)
    """
    
    @staticmethod
    def calculate_cosine_similarity(vector_a: List[float], vector_b: List[float]) -> Dict[str, float]:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vector_a: First feature vector
            vector_b: Second feature vector
            
        Returns:
            {
                'similarity_score': float (0-1),
                'percentage': float (0-100)
            }
            
        Raises:
            ValueError: If vectors have different lengths or are invalid
        """
        # Validate inputs
        if not vector_a or not vector_b:
            raise ValueError("Vectors cannot be empty")
        
        if len(vector_a) != len(vector_b):
            raise ValueError(
                f"Vector length mismatch: {len(vector_a)} vs {len(vector_b)}"
            )
        
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        
        # Calculate magnitudes
        magnitude_a = math.sqrt(sum(a * a for a in vector_a))
        magnitude_b = math.sqrt(sum(b * b for b in vector_b))
        
        # Handle zero vectors
        if magnitude_a == 0 or magnitude_b == 0:
            return {
                'similarity_score': 0.0,
                'percentage': 0.0
            }
        
        # Calculate cosine similarity
        similarity = dot_product / (magnitude_a * magnitude_b)
        
        # Clamp to [0, 1] range (handle floating point errors)
        similarity = max(0.0, min(1.0, similarity))
        
        return {
            'similarity_score': round(similarity, 4),
            'percentage': round(similarity * 100, 2)
        }
    
    @staticmethod
    def calculate_euclidean_similarity(vector_a: List[float], vector_b: List[float]) -> Dict[str, float]:
        """
        Calculate similarity using normalized Euclidean distance
        
        Alternative similarity metric for comparison
        
        Args:
            vector_a: First feature vector
            vector_b: Second feature vector
            
        Returns:
            {
                'similarity_score': float (0-1),
                'percentage': float (0-100)
            }
        """
        if not vector_a or not vector_b:
            raise ValueError("Vectors cannot be empty")
        
        if len(vector_a) != len(vector_b):
            raise ValueError(
                f"Vector length mismatch: {len(vector_a)} vs {len(vector_b)}"
            )
        
        # Calculate Euclidean distance
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(vector_a, vector_b)))
        
        # Normalize by maximum possible distance
        max_distance = math.sqrt(len(vector_a))
        
        # Convert distance to similarity (0 = identical, max = completely different)
        similarity = 1.0 - (distance / max_distance)
        similarity = max(0.0, min(1.0, similarity))
        
        return {
            'similarity_score': round(similarity, 4),
            'percentage': round(similarity * 100, 2)
        }
    
    @classmethod
    def compare_vectors(cls, vector_a: List[float], vector_b: List[float], 
                       method: str = 'cosine') -> Dict[str, Union[float, str]]:
        """
        Compare two vectors using specified similarity method
        
        Args:
            vector_a: First feature vector
            vector_b: Second feature vector
            method: 'cosine' or 'euclidean' (default: 'cosine')
            
        Returns:
            {
                'method': str,
                'similarity_score': float (0-1),
                'percentage': float (0-100),
                'interpretation': str
            }
        """
        if method == 'cosine':
            result = cls.calculate_cosine_similarity(vector_a, vector_b)
        elif method == 'euclidean':
            result = cls.calculate_euclidean_similarity(vector_a, vector_b)
        else:
            raise ValueError(f"Unknown method: {method}. Use 'cosine' or 'euclidean'")
        
        # Add interpretation
        percentage = result['percentage']
        if percentage >= 90:
            interpretation = "Extremely high compatibility"
        elif percentage >= 75:
            interpretation = "High compatibility"
        elif percentage >= 60:
            interpretation = "Moderate compatibility"
        elif percentage >= 40:
            interpretation = "Low compatibility"
        else:
            interpretation = "Very low compatibility"
        
        return {
            'method': method,
            'similarity_score': result['similarity_score'],
            'percentage': result['percentage'],
            'interpretation': interpretation
        }
