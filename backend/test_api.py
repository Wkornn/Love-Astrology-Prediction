"""
API Testing Script
Demonstrates all three mode endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_mode1():
    """Test Mode 1: Single-person love reading"""
    print("=" * 60)
    print("TEST MODE 1: Love Reading")
    print("=" * 60)
    
    payload = {
        "birth_data": {
            "date": "1990-01-15",
            "time": "14:30",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "UTC"
        }
    }
    
    response = requests.post(f"{BASE_URL}/mode1/love-reading", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✓ Success!")
        print(f"\nLove Profile:")
        for key, value in result['love_profile'].items():
            print(f"  {key}: {value:.1f}%")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(response.text)

def test_mode2():
    """Test Mode 2: Celebrity matching"""
    print("\n" + "=" * 60)
    print("TEST MODE 2: Celebrity Match")
    print("=" * 60)
    
    payload = {
        "birth_data": {
            "date": "1995-03-20",
            "time": "15:30",
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        "top_n": 3
    }
    
    response = requests.post(f"{BASE_URL}/mode2/celebrity-match", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✓ Success!")
        print(f"\nTop {len(result['matches'])} Matches:")
        for i, match in enumerate(result['matches'], 1):
            print(f"\n  {i}. {match['name']}")
            print(f"     Similarity: {match['similarity_score']:.1f}%")
            print(f"     Reason: {match['match_reason']}")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(response.text)

def test_mode3():
    """Test Mode 3: Couple compatibility"""
    print("\n" + "=" * 60)
    print("TEST MODE 3: Couple Match")
    print("=" * 60)
    
    payload = {
        "person1": {
            "date": "1990-01-15",
            "time": "14:30",
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        "person2": {
            "date": "1992-06-20",
            "time": "09:15",
            "latitude": 34.0522,
            "longitude": -118.2437
        }
    }
    
    response = requests.post(f"{BASE_URL}/mode3/couple-match", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✓ Success!")
        print(f"\nOverall Score: {result['overall_score']:.1f}%")
        print(f"\nComponents:")
        print(f"  Vector: {result['vector_component']:.1f}%")
        print(f"  Rules: {result['rule_component']:.1f}%")
        print(f"\nIndices:")
        print(f"  Emotional Sync: {result['emotional_sync']:.1f}%")
        print(f"  Chemistry: {result['chemistry_index']:.1f}%")
        print(f"  Stability: {result['stability_index']:.1f}%")
        
        if result['strengths']:
            print(f"\nStrengths:")
            for s in result['strengths']:
                print(f"  + {s}")
        
        if result['challenges']:
            print(f"\nChallenges:")
            for c in result['challenges']:
                print(f"  - {c}")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(response.text)

def print_curl_examples():
    """Print curl command examples"""
    print("\n" + "=" * 60)
    print("CURL EXAMPLES")
    print("=" * 60)
    
    print("\n# Mode 1: Love Reading")
    print("""curl -X POST http://localhost:8000/api/mode1/love-reading \\
  -H "Content-Type: application/json" \\
  -d '{
    "birth_data": {
      "date": "1990-01-15",
      "time": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060
    }
  }'""")
    
    print("\n# Mode 2: Celebrity Match")
    print("""curl -X POST http://localhost:8000/api/mode2/celebrity-match \\
  -H "Content-Type: application/json" \\
  -d '{
    "birth_data": {
      "date": "1995-03-20",
      "time": "15:30",
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "top_n": 5
  }'""")
    
    print("\n# Mode 3: Couple Match")
    print("""curl -X POST http://localhost:8000/api/mode3/couple-match \\
  -H "Content-Type: application/json" \\
  -d '{
    "person1": {
      "date": "1990-01-15",
      "time": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "person2": {
      "date": "1992-06-20",
      "time": "09:15",
      "latitude": 34.0522,
      "longitude": -118.2437
    }
  }'""")

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Love Debugging Lab v2.0 - API Tests")
    print("=" * 60)
    print("\nMake sure server is running: uvicorn app.main:app --reload")
    print()
    
    try:
        # Check if server is running
        response = requests.get("http://localhost:8000/health")
        if response.status_code != 200:
            print("✗ Server not responding")
            return
        
        test_mode1()
        test_mode2()
        test_mode3()
        print_curl_examples()
        
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        print("\nStart server with:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
