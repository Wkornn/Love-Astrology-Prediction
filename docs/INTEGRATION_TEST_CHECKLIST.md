# Integration Test Checklist - Love Debugging Lab v2.0

## Test Environment Setup
```bash
# Start backend
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Base URL
BASE_URL="http://localhost:8000"
```

---

## Test 1: Mode 1 - Single Person Love Reading

### Request
```bash
curl -X POST "$BASE_URL/api/mode1/love-reading" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "2005-03-21",
      "time": "09:58",
      "latitude": 40.0,
      "longitude": 75.0,
      "timezone": "UTC"
    },
    "debug": true
  }'
```

### Expected Output
```json
{
  "status": "success",
  "mode": "mode1",
  "data": {
    "love_profile": {
      "love_readiness": 30.0,
      "emotional_maturity": 94.0,
      "relationship_focus": 39.0,
      "passion_level": 45.0,
      "stability_potential": 20.0
    },
    "personality_vector": {
      "venus_mars_harmony": 0.3,
      "sun_moon_balance": 1.0,
      "moon_stability": 0.9,
      "fire_score": 0.6,
      "earth_score": 0.0,
      "air_score": 0.2,
      "water_score": 0.2,
      "hard_aspect_density": 0.0,
      "soft_aspect_density": 0.8,
      "seventh_house_strength": 0.3,
      "venus_element": 0.5,
      "mars_element": 1.0,
      "aspect_quality": 1.0,
      "fixed_score": 0.2,
      "cardinal_score": 0.2,
      "mutable_score": 0.6
    },
    "debug": {
      "aspects": [
        {
          "planet_a": "Sun",
          "planet_b": "Venus",
          "aspect": "Conjunction",
          "orb": 5.79,
          "exact_angle": 5.79,
          "strength": 0.28
        }
      ],
      "aspect_scores": {
        "total_score": 2.52,
        "harmonious_count": 4,
        "challenging_count": 0,
        "neutral_count": 0,
        "average_strength": 0.63
      }
    }
  },
  "diagnostics": {
    "bugs": [],
    "system_status": "OPTIMAL",
    "drama_risk_level": null,
    "recommendation_summary": "Strong foundation for relationships"
  },
  "timestamp": "2024-XX-XXTXX:XX:XX.XXXXXXZ"
}
```

### Success Criteria
- ✅ `status` = "success"
- ✅ `love_profile` values are NOT all 50.0
- ✅ `personality_vector` values are NOT all 0.5
- ✅ `debug.aspects` array has length > 0
- ✅ `debug.aspect_scores.harmonious_count` >= 0
- ✅ Response time < 2 seconds

---

## Test 2: Mode 2 - Celebrity Match (Empty DB → Mock Fallback)

### Request
```bash
curl -X POST "$BASE_URL/api/mode2/celebrity-match" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1995-06-15",
      "time": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "timezone": "America/New_York"
    },
    "top_n": 5,
    "debug": false
  }'
```

### Expected Output
```json
{
  "status": "success",
  "mode": "mode2",
  "data": {
    "matches": [
      {
        "name": "Taylor Swift",
        "occupation": "Singer-Songwriter",
        "similarity_score": 75.5,
        "match_reason": "Similar romantic expression"
      },
      {
        "name": "Elon Musk",
        "occupation": "Entrepreneur",
        "similarity_score": 68.2,
        "match_reason": "Compatible communication style"
      }
    ],
    "user_vector": {
      "venus_mars_harmony": 0.3,
      "sun_moon_balance": 1.0,
      "fire_score": 0.0,
      "earth_score": 0.2
    },
    "total_celebrities": 7
  },
  "diagnostics": {
    "bugs": [],
    "system_status": null,
    "drama_risk_level": null,
    "recommendation_summary": null
  },
  "timestamp": "2024-XX-XXTXX:XX:XX.XXXXXXZ"
}
```

### Success Criteria
- ✅ `status` = "success"
- ✅ `data.matches` array has 5 or 7 entries (mock data)
- ✅ `data.total_celebrities` = 7 (mock fallback count)
- ✅ Each match has `name`, `occupation`, `similarity_score`, `match_reason`
- ✅ `similarity_score` values are between 0-100
- ✅ Mock celebrities include: Taylor Swift, Elon Musk, Beyoncé, etc.

---

## Test 3: Mode 3 - Couple Compatibility

### Request
```bash
curl -X POST "$BASE_URL/api/mode3/couple-match" \
  -H "Content-Type: application/json" \
  -d '{
    "person1": {
      "date": "2005-03-21",
      "time": "09:58",
      "latitude": 40.0,
      "longitude": 75.0,
      "timezone": "UTC"
    },
    "person2": {
      "date": "1995-06-15",
      "time": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "timezone": "America/New_York"
    },
    "debug": false
  }'
```

### Expected Output
```json
{
  "status": "success",
  "mode": "mode3",
  "data": {
    "overall_score": 66.53,
    "vector_component": 70.89,
    "rule_component": 58.5,
    "emotional_sync": 94.0,
    "chemistry_index": 30.0,
    "stability_index": 24.0,
    "strengths": [
      "Compatible romantic and passionate expression",
      "Strong emotional synchronization"
    ],
    "challenges": [
      "Different Fire expression - requires compromise",
      "Different Air expression - requires compromise",
      "Relationship stability requires work"
    ]
  },
  "diagnostics": {
    "bugs": [
      {
        "code": "CHEMISTRY_LOW_301",
        "severity": "WARNING",
        "message": "Chemistry index below optimal threshold",
        "recommendation": "Focus on shared activities"
      }
    ],
    "system_status": "MODERATE",
    "drama_risk_level": "LOW",
    "recommendation_summary": "Solid foundation with growth areas"
  },
  "timestamp": "2024-XX-XXTXX:XX:XX.XXXXXXZ"
}
```

### Success Criteria
- ✅ `status` = "success"
- ✅ `overall_score` is NOT 50.0
- ✅ `emotional_sync`, `chemistry_index`, `stability_index` are between 0-100
- ✅ `strengths` array has 1-3 items
- ✅ `challenges` array has 1-3 items
- ✅ `vector_component` and `rule_component` are present

---

## Test 4: Invalid Request - Missing Time

### Request
```bash
curl -X POST "$BASE_URL/api/mode1/love-reading" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "2005-03-21",
      "latitude": 40.0,
      "longitude": 75.0,
      "timezone": "UTC"
    }
  }'
```

### Expected Output
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "birth_data", "time"],
      "msg": "Field required",
      "input": {
        "date": "2005-03-21",
        "latitude": 40.0,
        "longitude": 75.0,
        "timezone": "UTC"
      }
    }
  ]
}
```

### Success Criteria
- ✅ HTTP Status Code = 422 (Unprocessable Entity)
- ✅ Response contains `detail` array
- ✅ Error indicates missing `time` field
- ✅ `loc` includes ["body", "birth_data", "time"]

---

## Test 5: Invalid Coordinates

### Request
```bash
curl -X POST "$BASE_URL/api/mode1/love-reading" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "2005-03-21",
      "time": "09:58",
      "latitude": 95.0,
      "longitude": 200.0,
      "timezone": "UTC"
    }
  }'
```

### Expected Output
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "birth_data", "latitude"],
      "msg": "Input should be less than or equal to 90"
    },
    {
      "type": "less_than_equal",
      "loc": ["body", "birth_data", "longitude"],
      "msg": "Input should be less than or equal to 180"
    }
  ]
}
```

### Success Criteria
- ✅ HTTP Status Code = 422 (Unprocessable Entity)
- ✅ Response contains validation errors for latitude and longitude
- ✅ Error messages indicate out-of-range values
- ✅ Latitude must be -90 to 90
- ✅ Longitude must be -180 to 180

---

## Test 6: Empty Celebrity Database Verification

### Request
```bash
# Check database stats
curl -X GET "$BASE_URL/api/mode2/celebrity-match" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1990-01-01",
      "time": "12:00",
      "latitude": 0.0,
      "longitude": 0.0,
      "timezone": "UTC"
    },
    "top_n": 10
  }'
```

### Expected Behavior
When database is empty, system should:
1. Detect empty database
2. Load 7 mock celebrities in-memory
3. Return mock matches without persisting to DB

### Expected Output
```json
{
  "status": "success",
  "mode": "mode2",
  "data": {
    "matches": [
      {"name": "Taylor Swift", "similarity_score": 72.5},
      {"name": "Elon Musk", "similarity_score": 68.3},
      {"name": "Beyoncé", "similarity_score": 65.1},
      {"name": "Leonardo DiCaprio", "similarity_score": 61.8},
      {"name": "Ariana Grande", "similarity_score": 58.9},
      {"name": "Barack Obama", "similarity_score": 55.2},
      {"name": "Rihanna", "similarity_score": 52.7}
    ],
    "total_celebrities": 7
  }
}
```

### Success Criteria
- ✅ Returns exactly 7 mock celebrities
- ✅ All mock names are present
- ✅ Similarity scores are calculated (not all same value)
- ✅ No database persistence occurs
- ✅ Subsequent requests return same mock data

---

## Test 7: Demo Safety Mode - Fallback Values

### Trigger Condition
Force a calculation error by using invalid internal data

### Expected Behavior
- System catches exception
- Returns fallback values (all 0.5 / 50%)
- Logs error but doesn't crash
- Returns HTTP 200 with fallback data

### Success Criteria
- ✅ No HTTP 500 errors
- ✅ Response contains fallback values
- ✅ `love_profile` all = 50.0
- ✅ `personality_vector` all = 0.5
- ✅ System remains operational

---

## Quick Test Script

```bash
#!/bin/bash
BASE_URL="http://localhost:8000"

echo "=== Test 1: Mode 1 ==="
curl -s -X POST "$BASE_URL/api/mode1/love-reading" \
  -H "Content-Type: application/json" \
  -d '{"birth_data":{"date":"2005-03-21","time":"09:58","latitude":40.0,"longitude":75.0,"timezone":"UTC"}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ PASS' if d['status']=='success' and d['data']['love_profile']['love_readiness']!=50.0 else '❌ FAIL')"

echo "=== Test 2: Mode 2 ==="
curl -s -X POST "$BASE_URL/api/mode2/celebrity-match" \
  -H "Content-Type: application/json" \
  -d '{"birth_data":{"date":"1995-06-15","time":"14:30","latitude":40.7128,"longitude":-74.0060,"timezone":"UTC"},"top_n":5}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ PASS' if d['status']=='success' and d['data']['total_celebrities']==7 else '❌ FAIL')"

echo "=== Test 3: Mode 3 ==="
curl -s -X POST "$BASE_URL/api/mode3/couple-match" \
  -H "Content-Type: application/json" \
  -d '{"person1":{"date":"2005-03-21","time":"09:58","latitude":40.0,"longitude":75.0,"timezone":"UTC"},"person2":{"date":"1995-06-15","time":"14:30","latitude":40.7128,"longitude":-74.0060,"timezone":"UTC"}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ PASS' if d['status']=='success' and d['data']['overall_score']!=50.0 else '❌ FAIL')"

echo "=== Test 4: Invalid Request ==="
curl -s -X POST "$BASE_URL/api/mode1/love-reading" \
  -H "Content-Type: application/json" \
  -d '{"birth_data":{"date":"2005-03-21","latitude":40.0,"longitude":75.0}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ PASS' if 'detail' in d else '❌ FAIL')"

echo "=== Test 5: Invalid Coordinates ==="
curl -s -X POST "$BASE_URL/api/mode1/love-reading" \
  -H "Content-Type: application/json" \
  -d '{"birth_data":{"date":"2005-03-21","time":"09:58","latitude":95.0,"longitude":200.0,"timezone":"UTC"}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ PASS' if 'detail' in d else '❌ FAIL')"

echo "=== All Tests Complete ==="
```

---

## Summary Checklist

- [ ] Test 1: Mode 1 returns real values (not 50%)
- [ ] Test 2: Mode 2 returns 7 mock celebrities
- [ ] Test 3: Mode 3 calculates compatibility correctly
- [ ] Test 4: Missing fields return 422 error
- [ ] Test 5: Invalid coordinates return 422 error
- [ ] Test 6: Empty DB triggers mock fallback
- [ ] Test 7: Demo Safety Mode prevents crashes
- [ ] All responses have correct JSON structure
- [ ] All timestamps are in ISO format
- [ ] No HTTP 500 errors occur
