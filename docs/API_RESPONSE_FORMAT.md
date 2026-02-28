# Standardized API Response Format

## Overview

All API endpoints now return responses in a consistent, standardized format.

## Response Structure

```json
{
  "status": "success" | "error",
  "mode": "mode1" | "mode2" | "mode3",
  "data": { ... },
  "diagnostics": {
    "bugs": [...],
    "system_status": "string",
    "drama_risk_level": "string",
    "recommendation_summary": "string"
  },
  "timestamp": "2024-02-28T12:34:56.789Z"
}
```

## Success Responses

### Mode 1: Love Reading

```json
{
  "status": "success",
  "mode": "mode1",
  "data": {
    "love_profile": {
      "romantic_readiness": 0.75,
      "passion_drive": 0.82,
      "emotional_depth": 0.68,
      "commitment_capacity": 0.71
    },
    "personality_vector": {
      "venus_mars_harmony": 0.82,
      "sun_moon_balance": 0.75,
      "moon_stability": 0.71,
      "fire_score": 0.65,
      "earth_score": 0.45,
      "air_score": 0.58,
      "water_score": 0.72,
      "hard_aspect_density": 0.38,
      "soft_aspect_density": 0.62
    }
  },
  "diagnostics": {
    "bugs": [
      {
        "code": "LOVE_VENUS_001",
        "severity": "INFO",
        "message": "Strong Venus placement detected",
        "recommendation": "Leverage natural charm"
      }
    ],
    "system_status": "READY - System optimized",
    "drama_risk_level": null,
    "recommendation_summary": "High compatibility potential"
  },
  "timestamp": "2024-02-28T12:34:56.789Z"
}
```

### Mode 2: Celebrity Match

```json
{
  "status": "success",
  "mode": "mode2",
  "data": {
    "matches": [
      {
        "name": "Alex Rivera",
        "occupation": "Musician",
        "similarity_score": 87.5,
        "match_reason": "Similar romantic expression"
      }
    ],
    "user_vector": {
      "venus_mars_harmony": 0.75,
      ...
    },
    "total_celebrities": 7
  },
  "diagnostics": {
    "bugs": [],
    "system_status": null,
    "drama_risk_level": null,
    "recommendation_summary": null
  },
  "timestamp": "2024-02-28T12:34:56.789Z"
}
```

### Mode 3: Couple Compatibility

```json
{
  "status": "success",
  "mode": "mode3",
  "data": {
    "overall_score": 78.5,
    "vector_component": 82.3,
    "rule_component": 74.7,
    "emotional_sync": 81.2,
    "chemistry_index": 76.8,
    "stability_index": 77.5,
    "strengths": [
      "Similar Fire energy",
      "Compatible romantic expression"
    ],
    "challenges": [
      "Different Earth expression",
      "Communication styles may clash"
    ]
  },
  "diagnostics": {
    "bugs": [
      {
        "code": "COMPAT_SYNC_001",
        "severity": "INFO",
        "message": "High compatibility score",
        "recommendation": "Maintain open communication"
      }
    ],
    "system_status": "OPTIMAL - All systems nominal",
    "drama_risk_level": "LOW - System stable",
    "recommendation_summary": "System analysis indicates high compatibility"
  },
  "timestamp": "2024-02-28T12:34:56.789Z"
}
```

## Error Responses

### Validation Error (400)

```json
{
  "status": "error",
  "mode": "mode1",
  "error": "Failed to generate love reading",
  "details": "Date must be in YYYY-MM-DD format",
  "timestamp": "2024-02-28T12:34:56.789Z"
}
```

### Internal Server Error (500)

```json
{
  "status": "error",
  "mode": null,
  "error": "Internal server error",
  "details": "An unexpected error occurred",
  "timestamp": "2024-02-28T12:34:56.789Z"
}
```

## Key Features

### ✅ Consistency
- All endpoints return same top-level structure
- `status`, `mode`, `data`, `diagnostics`, `timestamp` always present

### ✅ Type Safety
- Pydantic models enforce strict typing
- Invalid responses caught at runtime

### ✅ Error Handling
- No raw Python exceptions leak to frontend
- All errors return standardized JSON
- Detailed error logging on backend

### ✅ Diagnostics
- Structured diagnostic information
- Severity levels: CRITICAL, WARNING, INFO
- Bug codes for tracking
- Recommendations for users

### ✅ Timestamps
- ISO 8601 format with UTC timezone
- Consistent across all responses

## Frontend Integration

### TypeScript Interface

```typescript
interface StandardResponse<T> {
  status: 'success' | 'error';
  mode: 'mode1' | 'mode2' | 'mode3';
  data: T;
  diagnostics: {
    bugs: DiagnosticBug[];
    system_status?: string;
    drama_risk_level?: string;
    recommendation_summary?: string;
  };
  timestamp: string;
}

interface DiagnosticBug {
  code: string;
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  message: string;
  recommendation: string;
}
```

### Error Handling

```typescript
try {
  const response = await api.post('/api/mode1/love-reading', data);
  if (response.data.status === 'success') {
    // Handle success
    console.log(response.data.data);
  }
} catch (error) {
  if (error.response?.data) {
    // Standardized error format
    const { status, error: errorMsg, details } = error.response.data;
    console.error(`${errorMsg}: ${details}`);
  }
}
```

## Changes Made

### Files Modified:
1. `app/api/schemas/responses.py` - Standardized response models
2. `app/api/routes/modes.py` - Updated endpoints to use new format
3. `app/api/service_orchestrator.py` - Ensured diagnostics always returns dict
4. `app/main.py` - Added global exception handler and logging

### Benefits:
- ✅ Consistent API contract
- ✅ Better error handling
- ✅ Easier frontend integration
- ✅ Production-ready error responses
- ✅ Comprehensive logging
