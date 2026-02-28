"""
Example usage of Aspect Engine
Demonstrates natal chart aspect detection
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.aspects.aspect_detector import AspectDetector
from services.aspects.aspect_scorer import AspectScorer
from services.chart.birth_chart import BirthChartCalculator
import json

def main():
    """Example: Detect aspects in a natal chart"""
    print("=" * 60)
    print("Love Debugging Lab v2.0 - Aspect Engine")
    print("=" * 60)
    print("\nNATAL CHART ASPECTS")
    print("=" * 60)
    
    try:
        # Calculate a birth chart
        calculator = BirthChartCalculator()
        chart = calculator.calculate_chart(
            date='1990-01-15',
            time='14:30',
            latitude=40.7128,
            longitude=-74.0060
        )
        
        # Extract planetary longitudes
        planets = {
            name: info['longitude'] 
            for name, info in chart['planets'].items()
        }
        
        print(f"\nPlanetary Positions:")
        for name, info in chart['planets'].items():
            print(f"  {name}: {info['sign']} {info['degree']:.1f}° (House {info['house']})")
        
        # Detect aspects
        detector = AspectDetector()
        result = detector.detect_aspects_json(planets)
        
        if result['success']:
            print(f"\n✓ Found {result['total_aspects']} aspects\n")
            
            for aspect in result['aspects']:
                print(f"  {aspect['planet_a']} {aspect['aspect']} {aspect['planet_b']}")
                print(f"    Orb: {aspect['orb']}° | Strength: {aspect['strength']:.2f}\n")
        
        # Score the aspects
        scorer = AspectScorer()
        aspects_obj = detector.detect_aspects(planets)
        scores = scorer.score_aspect_list(aspects_obj)
        
        print("Aspect Quality Analysis:")
        print(f"  Total Score: {scores['total_score']}")
        print(f"  Harmonious Aspects: {scores['harmonious_count']}")
        print(f"  Challenging Aspects: {scores['challenging_count']}")
        print(f"  Neutral Aspects: {scores['neutral_count']}")
        print(f"  Average Strength: {scores['average_strength']}")
        
        # Show strongest aspects
        if aspects_obj:
            print("\nStrongest Aspects:")
            strongest = scorer.get_strongest_aspects(aspects_obj, top_n=3)
            for i, aspect in enumerate(strongest, 1):
                score = scorer.score_aspect(aspect)
                quality = "Harmonious" if score > 0 else "Challenging" if score < 0 else "Neutral"
                print(f"  {i}. {aspect.planet_a} {aspect.aspect_type.name} {aspect.planet_b}")
                print(f"     Strength: {aspect.strength:.2f} | Quality: {quality} ({score:+.2f})")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
