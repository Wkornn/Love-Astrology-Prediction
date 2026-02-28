# Debug Mode Documentation

## Overview

Optional debug flag exposes internal calculation data for development and testing.

## Usage

### Request Format

Add `"debug": true` to any mode request:

```json
{
  "birth_data": {
    "date": "1990-06-15",
    "time": "14:30",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "debug": true
}
```

### Default Behavior

If `debug` is not provided or set to `false`, internal data is NOT exposed.

## Debug Data Exposed

### Mode 1: Love Reading

**Additional Fields**:
```json
{
  "debug": {
    "raw_feature_vector": [0.75, 0.82, 0.68, ...],
    "feature_labels": ["venus_mars_harmony", "sun_moon_balance", ...],
    "vector_length": 9
  }
}
```

### Mode 2: Celebrity Match

**Additional Fields**:
```json
{
  "debug": {
    "raw_feature_vector": [0.75, 0.82, 0.68, ...],
    "feature_labels": ["venus_mars_harmony", "sun_moon_balance", ...],
    "raw_similarity_scores": [87.5, 84.2, 81.8, ...]
  }
}
```

### Mode 3: Couple Compatibility

**Additional Fields**:
```json
{
  "debug": {
    "person1_raw_vector": [0.75, 0.82, 0.68, ...],
    "person2_raw_vector": [0.68, 0.71, 0.79, ...],
    "feature_labels": ["venus_mars_harmony", "sun_moon_balance", ...],
    "cosine_similarity_raw": 0.8523,
    "cosine_similarity_percentage": 85.23,
    "rule_based_score": 74.5,
    "hard_aspect_density_p1": 0.38,
    "hard_aspect_density_p2": 0.42,
    "soft_aspect_density_p1": 0.62,
    "soft_aspect_density_p2": 0.58
  }
}
```

## Example Requests

### Mode 1 with Debug
```bash
curl -X POST http://localhost:8000/api/mode1/love-reading \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1990-06-15",
      "time": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "debug": true
  }'
```

### Mode 3 with Debug
```bash
curl -X POST http://localhost:8000/api/mode3/couple-match \
  -H "Content-Type: application/json" \
  -d '{
    "person1": {
      "date": "1990-06-15",
      "time": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "person2": {
      "date": "1992-03-20",
      "time": "10:00",
      "latitude": 34.0522,
      "longitude": -118.2437
    },
    "debug": true
  }'
```

## Use Cases

### Development
- Verify feature vector calculations
- Debug similarity algorithm
- Validate aspect detection
- Test rule-based scoring

### Testing
- Compare expected vs actual vectors
- Verify cosine similarity math
- Check aspect density calculations
- Validate compatibility formulas

### Debugging
- Investigate unexpected results
- Trace calculation steps
- Verify data transformations
- Analyze edge cases

## Security Considerations

### ✅ Safe to Use
- Debug data is computational, not personal
- No sensitive user information exposed
- Only mathematical calculations shown

### ⚠️ Production Recommendations
1. **Disable in production** - Set `debug: false` by default
2. **Rate limit debug requests** - Prevent abuse
3. **Log debug usage** - Monitor who uses debug mode
4. **Require authentication** - Only allow authorized users

## Implementation Details

### Request Schema
```python
class Mode1Request(BaseModel):
    birth_data: BirthDataRequest
    debug: Optional[bool] = Field(False, description="Include debug information")
```

### Service Orchestrator
```python
def execute_mode1(self, birth_data: Dict, debug: bool = False) -> Dict:
    result = {...}
    
    if debug:
        result['debug'] = {
            'raw_feature_vector': vector_data['feature_vector'],
            'feature_labels': self.vector_builder.FEATURE_LABELS,
            'vector_length': len(vector_data['feature_vector'])
        }
    
    return result
```

## Feature Vector Labels

The 9-dimensional feature vector contains:
1. `venus_mars_harmony` - Romantic/passion alignment
2. `sun_moon_balance` - Ego/emotion balance
3. `moon_stability` - Emotional stability
4. `fire_score` - Fire element strength
5. `earth_score` - Earth element strength
6. `air_score` - Air element strength
7. `water_score` - Water element strength
8. `hard_aspect_density` - Challenging aspects
9. `soft_aspect_density` - Harmonious aspects

## Benefits

✅ **Transparency** - See how calculations work
✅ **Debugging** - Identify issues quickly
✅ **Validation** - Verify algorithm correctness
✅ **Learning** - Understand astrology math
✅ **Testing** - Compare expected vs actual

## Limitations

⚠️ **Not user-friendly** - Raw data, not interpretations
⚠️ **Requires knowledge** - Need to understand vectors
⚠️ **Extra data** - Increases response size
⚠️ **Performance** - Slight overhead (minimal)

## Summary

- **Default**: `debug: false` - No internal data exposed
- **Enabled**: `debug: true` - Full internal data included
- **Use for**: Development, testing, debugging
- **Production**: Disable or restrict access

**Status**: ✅ Debug mode implemented and ready for use!
