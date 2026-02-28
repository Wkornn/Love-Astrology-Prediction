#!/bin/bash

BASE_URL="http://localhost:8000"
PASS=0
FAIL=0

echo "======================================"
echo "Integration Test Suite"
echo "Love Debugging Lab v2.0"
echo "======================================"
echo ""

# Test 1: Mode 1
echo "Test 1: Mode 1 - Single Person Love Reading"
RESPONSE=$(curl -s -X POST "$BASE_URL/api/mode1/love-reading" \
  -H "Content-Type: application/json" \
  -d '{"birth_data":{"date":"2005-03-21","time":"09:58","latitude":40.0,"longitude":75.0,"timezone":"UTC"},"debug":true}')

STATUS=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status',''))" 2>/dev/null)
LOVE_READY=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['love_profile']['love_readiness'])" 2>/dev/null)
ASPECTS=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data'].get('debug',{}).get('aspects',[])))" 2>/dev/null)

if [ "$STATUS" = "success" ] && [ "$LOVE_READY" != "50.0" ] && [ "$ASPECTS" -gt "0" ]; then
  echo "✅ PASS - Real values returned, aspects detected"
  ((PASS++))
else
  echo "❌ FAIL - Status: $STATUS, Love Ready: $LOVE_READY, Aspects: $ASPECTS"
  ((FAIL++))
fi
echo ""

# Test 2: Mode 2
echo "Test 2: Mode 2 - Celebrity Match (Mock Fallback)"
RESPONSE=$(curl -s -X POST "$BASE_URL/api/mode2/celebrity-match" \
  -H "Content-Type: application/json" \
  -d '{"birth_data":{"date":"1995-06-15","time":"14:30","latitude":40.7128,"longitude":-74.0060,"timezone":"UTC"},"top_n":5}')

STATUS=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status',''))" 2>/dev/null)
TOTAL=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['total_celebrities'])" 2>/dev/null)

if [ "$STATUS" = "success" ] && [ "$TOTAL" = "7" ]; then
  echo "✅ PASS - Mock celebrities loaded"
  ((PASS++))
else
  echo "❌ FAIL - Status: $STATUS, Total: $TOTAL"
  ((FAIL++))
fi
echo ""

# Test 3: Mode 3
echo "Test 3: Mode 3 - Couple Compatibility"
RESPONSE=$(curl -s -X POST "$BASE_URL/api/mode3/couple-match" \
  -H "Content-Type: application/json" \
  -d '{"person1":{"date":"2005-03-21","time":"09:58","latitude":40.0,"longitude":75.0,"timezone":"UTC"},"person2":{"date":"1995-06-15","time":"14:30","latitude":40.7128,"longitude":-74.0060,"timezone":"UTC"}}')

STATUS=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status',''))" 2>/dev/null)
SCORE=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['overall_score'])" 2>/dev/null)

if [ "$STATUS" = "success" ] && [ "$SCORE" != "50.0" ]; then
  echo "✅ PASS - Compatibility calculated (Score: $SCORE%)"
  ((PASS++))
else
  echo "❌ FAIL - Status: $STATUS, Score: $SCORE"
  ((FAIL++))
fi
echo ""

# Test 4: Invalid Request
echo "Test 4: Invalid Request - Missing Time"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/mode1/love-reading" \
  -H "Content-Type: application/json" \
  -d '{"birth_data":{"date":"2005-03-21","latitude":40.0,"longitude":75.0}}')

if [ "$HTTP_CODE" = "422" ]; then
  echo "✅ PASS - Validation error returned (422)"
  ((PASS++))
else
  echo "❌ FAIL - HTTP Code: $HTTP_CODE (expected 422)"
  ((FAIL++))
fi
echo ""

# Test 5: Invalid Coordinates
echo "Test 5: Invalid Coordinates"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/mode1/love-reading" \
  -H "Content-Type: application/json" \
  -d '{"birth_data":{"date":"2005-03-21","time":"09:58","latitude":95.0,"longitude":200.0,"timezone":"UTC"}}')

if [ "$HTTP_CODE" = "422" ]; then
  echo "✅ PASS - Validation error returned (422)"
  ((PASS++))
else
  echo "❌ FAIL - HTTP Code: $HTTP_CODE (expected 422)"
  ((FAIL++))
fi
echo ""

# Test 6: Health Check
echo "Test 6: Health Check"
RESPONSE=$(curl -s "$BASE_URL/health")
STATUS=$(echo $RESPONSE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status',''))" 2>/dev/null)

if [ "$STATUS" = "healthy" ]; then
  echo "✅ PASS - Server healthy"
  ((PASS++))
else
  echo "❌ FAIL - Status: $STATUS"
  ((FAIL++))
fi
echo ""

# Summary
echo "======================================"
echo "Test Results"
echo "======================================"
echo "✅ Passed: $PASS"
echo "❌ Failed: $FAIL"
echo "Total: $((PASS + FAIL))"
echo ""

if [ $FAIL -eq 0 ]; then
  echo "🎉 All tests passed!"
  exit 0
else
  echo "⚠️  Some tests failed"
  exit 1
fi
