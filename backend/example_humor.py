"""
Example usage of Humor Intelligence Layer
Demonstrates diagnostic-style humor generation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.intelligence.humor_intelligence import HumorIntelligence

def test_compatibility_diagnostics():
    """Test compatibility analysis diagnostics"""
    print("=" * 60)
    print("COMPATIBILITY DIAGNOSTICS")
    print("=" * 60)
    
    test_cases = [
        {
            'name': 'High Compatibility, Low Drama',
            'overall_score': 85.0,
            'hard_aspect_density': 0.2,
            'emotional_stability': 0.8
        },
        {
            'name': 'Moderate Compatibility, High Tension',
            'overall_score': 62.0,
            'hard_aspect_density': 0.7,
            'emotional_stability': 0.5
        },
        {
            'name': 'Low Compatibility, Volatile',
            'overall_score': 38.0,
            'hard_aspect_density': 0.6,
            'emotional_stability': 0.3
        }
    ]
    
    humor = HumorIntelligence()
    
    for case in test_cases:
        print(f"\n{'─' * 60}")
        print(f"Test Case: {case['name']}")
        print(f"{'─' * 60}")
        print(f"Overall Score: {case['overall_score']:.1f}%")
        print(f"Hard Aspect Density: {case['hard_aspect_density']:.2f}")
        print(f"Emotional Stability: {case['emotional_stability']:.2f}")
        
        result = humor.analyze_compatibility(
            case['overall_score'],
            case['hard_aspect_density'],
            case['emotional_stability']
        )
        
        print(f"\n📊 System Status: {result['system_status']}")
        print(f"⚠️  Drama Risk: {result['drama_risk_level']}")
        
        print(f"\n🐛 Love Bugs Detected ({len(result['bugs'])}):")
        for bug in result['bugs']:
            severity_icon = {
                'CRITICAL': '🔴',
                'WARNING': '🟡',
                'INFO': '🟢'
            }
            print(f"\n  {severity_icon[bug['severity']]} [{bug['severity']}] {bug['code']}")
            print(f"     {bug['message']}")
            print(f"     → {bug['recommendation']}")
        
        print(f"\n💡 Recommendation:")
        print(f"   {result['recommendation_summary']}")

def test_single_chart_diagnostics():
    """Test single chart analysis diagnostics"""
    print("\n" + "=" * 60)
    print("SINGLE CHART DIAGNOSTICS")
    print("=" * 60)
    
    test_profiles = [
        {
            'name': 'High Readiness Profile',
            'love_profile': {
                'love_readiness': 85.0,
                'emotional_maturity': 78.0,
                'relationship_focus': 72.0,
                'passion_level': 80.0,
                'stability_potential': 70.0
            },
            'personality_vector': {
                'venus_mars_harmony': 0.8,
                'moon_stability': 0.7
            }
        },
        {
            'name': 'Developing Profile',
            'love_profile': {
                'love_readiness': 45.0,
                'emotional_maturity': 55.0,
                'relationship_focus': 50.0,
                'passion_level': 85.0,
                'stability_potential': 35.0
            },
            'personality_vector': {
                'venus_mars_harmony': 0.6,
                'moon_stability': 0.4
            }
        }
    ]
    
    humor = HumorIntelligence()
    
    for profile in test_profiles:
        print(f"\n{'─' * 60}")
        print(f"Profile: {profile['name']}")
        print(f"{'─' * 60}")
        
        for key, value in profile['love_profile'].items():
            print(f"{key:25s} {value:.1f}%")
        
        result = humor.analyze_single_chart(
            profile['love_profile'],
            profile['personality_vector']
        )
        
        print(f"\n📊 System Status: {result['system_status']}")
        
        print(f"\n🐛 Diagnostics ({len(result['bugs'])}):")
        for bug in result['bugs']:
            severity_icon = {
                'CRITICAL': '🔴',
                'WARNING': '🟡',
                'INFO': '🟢'
            }
            print(f"\n  {severity_icon[bug['severity']]} [{bug['severity']}] {bug['code']}")
            print(f"     {bug['message']}")
            print(f"     → {bug['recommendation']}")
        
        print(f"\n💡 Recommendation:")
        print(f"   {result['recommendation_summary']}")

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Love Debugging Lab v2.0 - Humor Intelligence")
    print("=" * 60)
    print()
    
    try:
        test_compatibility_diagnostics()
        test_single_chart_diagnostics()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
