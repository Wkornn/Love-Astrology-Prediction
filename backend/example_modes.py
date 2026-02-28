"""
Example usage of Mode Controller
Demonstrates all 3 operational modes
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.modes.mode_controller import ModeController
import json

def example_mode_1():
    """Mode 1: Single-person love reading"""
    print("\n" + "=" * 60)
    print("MODE 1: SINGLE-PERSON LOVE READING")
    print("=" * 60)
    
    controller = ModeController()
    
    input_data = {
        'date': '1990-01-15',
        'time': '14:30',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'timezone': 'UTC'
    }
    
    result = controller.execute_mode('single_person', input_data)
    
    if result['success']:
        profile = result['result']['love_profile']
        print(f"\n✓ Love Profile Generated")
        print(f"  Dominant Element: {profile['dominant_element']}")
        print(f"  Love Style: {profile['love_style']}")
        print(f"  Emotional Intensity: {profile['emotional_intensity']}")
        print(f"  Venus-Mars Harmony: {profile['venus_mars_harmony']}")
        print(f"  Relationship Stability: {profile['relationship_stability']}")
    else:
        print(f"✗ Error: {result['error']}")

def example_mode_2():
    """Mode 2: Celebrity matching"""
    print("\n" + "=" * 60)
    print("MODE 2: CELEBRITY MATCHING")
    print("=" * 60)
    
    controller = ModeController()
    
    input_data = {
        'date': '1990-01-15',
        'time': '14:30',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'timezone': 'UTC',
        'top_n': 3
    }
    
    result = controller.execute_mode('celebrity_matching', input_data)
    
    if result['success']:
        matches = result['result']['matches']
        print(f"\n✓ Top {len(matches)} Celebrity Matches:")
        for i, match in enumerate(matches, 1):
            print(f"\n  {i}. {match['name']}")
            print(f"     Similarity: {match['similarity_score']}%")
            print(f"     Reason: {match['match_reason']}")
    else:
        print(f"✗ Error: {result['error']}")

def example_mode_3():
    """Mode 3: Couple compatibility"""
    print("\n" + "=" * 60)
    print("MODE 3: COUPLE COMPATIBILITY")
    print("=" * 60)
    
    controller = ModeController()
    
    input_data = {
        'person1': {
            'date': '1990-01-15',
            'time': '14:30',
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        'person2': {
            'date': '1992-06-20',
            'time': '09:15',
            'latitude': 34.0522,
            'longitude': -118.2437
        }
    }
    
    result = controller.execute_mode('couple_compatibility', input_data)
    
    if result['success']:
        data = result['result']
        print(f"\n✓ Compatibility Analysis Complete")
        print(f"  Overall Similarity: {data['similarity_score']}%")
        print(f"\n  Breakdown:")
        for category, score in data['compatibility_breakdown'].items():
            print(f"    {category.capitalize()}: {score}%")
        
        print(f"\n  Strengths:")
        for strength in data['strengths']:
            print(f"    + {strength}")
        
        print(f"\n  Challenges:")
        for challenge in data['challenges']:
            print(f"    - {challenge}")
    else:
        print(f"✗ Error: {result['error']}")

def show_available_modes():
    """Show all available modes"""
    print("\n" + "=" * 60)
    print("AVAILABLE MODES")
    print("=" * 60)
    
    controller = ModeController()
    modes = controller.get_available_modes()
    
    for mode in modes:
        print(f"\n  {mode['name']}")
        print(f"    {mode['description']}")

def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Love Debugging Lab v2.0 - Mode Controller")
    print("=" * 60)
    
    try:
        show_available_modes()
        example_mode_1()
        example_mode_2()
        example_mode_3()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
