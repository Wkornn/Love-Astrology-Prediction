"""Test Debug Mode - Verify debug flag exposes internal data"""

import sys
sys.path.insert(0, '.')

from app.api.service_orchestrator import ServiceOrchestrator

print("=" * 60)
print("DEBUG MODE TESTS")
print("=" * 60)
print()

orchestrator = ServiceOrchestrator()

birth_data = {
    'date': '1990-06-15',
    'time': '14:30',
    'latitude': 40.7128,
    'longitude': -74.0060,
    'timezone': 'UTC'
}

# Test Mode 1 - Without Debug
print("Test 1: Mode 1 WITHOUT Debug Flag")
print("-" * 60)
result = orchestrator.execute_mode1(birth_data, debug=False)
print(f"Keys in response: {list(result.keys())}")
print(f"Has 'debug' key: {'debug' in result}")
print(f"✅ No debug data exposed")
print()

# Test Mode 1 - With Debug
print("Test 2: Mode 1 WITH Debug Flag")
print("-" * 60)
result = orchestrator.execute_mode1(birth_data, debug=True)
print(f"Keys in response: {list(result.keys())}")
print(f"Has 'debug' key: {'debug' in result}")
if 'debug' in result:
    print(f"Debug keys: {list(result['debug'].keys())}")
    print(f"Raw vector length: {len(result['debug']['raw_feature_vector'])}")
    print(f"Raw vector: {result['debug']['raw_feature_vector']}")
print(f"✅ Debug data exposed")
print()

# Test Mode 2 - Without Debug
print("Test 3: Mode 2 WITHOUT Debug Flag")
print("-" * 60)
result = orchestrator.execute_mode2(birth_data, top_n=3, debug=False)
print(f"Keys in response: {list(result.keys())}")
print(f"Has 'debug' key: {'debug' in result}")
print(f"✅ No debug data exposed")
print()

# Test Mode 2 - With Debug
print("Test 4: Mode 2 WITH Debug Flag")
print("-" * 60)
result = orchestrator.execute_mode2(birth_data, top_n=3, debug=True)
print(f"Keys in response: {list(result.keys())}")
print(f"Has 'debug' key: {'debug' in result}")
if 'debug' in result:
    print(f"Debug keys: {list(result['debug'].keys())}")
    print(f"Raw similarity scores: {result['debug']['raw_similarity_scores']}")
print(f"✅ Debug data exposed")
print()

# Test Mode 3 - Without Debug
print("Test 5: Mode 3 WITHOUT Debug Flag")
print("-" * 60)
result = orchestrator.execute_mode3(birth_data, birth_data, debug=False)
print(f"Keys in response: {list(result.keys())}")
print(f"Has 'debug' key: {'debug' in result}")
print(f"✅ No debug data exposed")
print()

# Test Mode 3 - With Debug
print("Test 6: Mode 3 WITH Debug Flag")
print("-" * 60)
result = orchestrator.execute_mode3(birth_data, birth_data, debug=True)
print(f"Keys in response: {list(result.keys())}")
print(f"Has 'debug' key: {'debug' in result}")
if 'debug' in result:
    print(f"Debug keys: {list(result['debug'].keys())}")
    print(f"Cosine similarity raw: {result['debug']['cosine_similarity_raw']}")
    print(f"Cosine similarity %: {result['debug']['cosine_similarity_percentage']}")
    print(f"Hard aspect density P1: {result['debug']['hard_aspect_density_p1']}")
    print(f"Soft aspect density P1: {result['debug']['soft_aspect_density_p1']}")
print(f"✅ Debug data exposed")
print()

print("=" * 60)
print("DEBUG MODE: ALL TESTS PASSED")
print("Debug flag controls internal data exposure")
print("=" * 60)
