"""
Example usage of Birth Chart Calculator
Run this to test the implementation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.chart.birth_chart import BirthChartCalculator
import json

def main():
    """Test birth chart calculation"""
    
    # Initialize calculator
    calculator = BirthChartCalculator()
    
    # Example: Calculate chart for someone born in New York
    # Date: January 15, 1990
    # Time: 14:30 (2:30 PM)
    # Location: New York City (40.7128° N, 74.0060° W)
    
    print("=" * 60)
    print("Love Debugging Lab v2.0 - Birth Chart Calculator")
    print("=" * 60)
    print()
    
    try:
        result = calculator.calculate_chart_json(
            date='1990-01-15',
            time='14:30',
            latitude=40.7128,
            longitude=-74.0060,
            timezone='UTC'
        )
        
        if result['success']:
            print("✓ Chart calculation successful!\n")
            print(json.dumps(result['data'], indent=2))
        else:
            print(f"✗ Error: {result['error']}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
