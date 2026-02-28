# Aspect Engine Module

## Overview

Production-grade aspect detection and scoring system for natal charts and synastry analysis.

## Architecture

```
services/aspects/
├── aspect_detector.py    # Core aspect detection logic
└── aspect_scorer.py      # Aspect quality evaluation
```

## Features

✅ **Aspect Detection**
- Conjunction (0° ± 8°)
- Opposition (180° ± 8°)
- Trine (120° ± 6°)
- Square (90° ± 6°)
- Sextile (60° ± 4°)

✅ **Strength Calculation**
- Exact aspects = 1.0 strength
- Wider orbs = lower strength
- Linear decay based on orb

✅ **Dual Mode Operation**
- Natal chart aspects (within single chart)
- Synastry aspects (cross-chart)

✅ **Quality Scoring**
- Harmonious aspects (+)
- Challenging aspects (-)
- Context-aware conjunction scoring

## Usage

### Natal Chart Aspects

```python
from services.aspects.aspect_detector import AspectDetector

# Planet longitudes from birth chart
planets = {
    'Sun': 294.5,
    'Moon': 120.3,
    'Venus': 310.2,
    'Mars': 45.8
}

detector = AspectDetector()
result = detector.detect_aspects_json(planets)

# Output:
# {
#   'success': True,
#   'aspect_type': 'natal',
#   'total_aspects': 3,
#   'aspects': [...]
# }
```

### Synastry Aspects

```python
chart1_planets = {'Sun': 120.0, 'Moon': 210.0, 'Venus': 150.0}
chart2_planets = {'Sun': 300.0, 'Moon': 30.0, 'Mars': 240.0}

result = detector.detect_aspects_json(chart1_planets, chart2_planets)
```

### Aspect Scoring

```python
from services.aspects.aspect_scorer import AspectScorer

scorer = AspectScorer()

# Score individual aspect
score = scorer.score_aspect(detected_aspect)  # -1.0 to +1.0

# Score list of aspects
aspects = detector.detect_natal_aspects(planets)
breakdown = scorer.score_aspect_list(aspects)

# Output:
# {
#   'total_score': 2.5,
#   'harmonious_count': 4,
#   'challenging_count': 2,
#   'neutral_count': 1,
#   'average_strength': 0.75
# }
```

## Design Principles

### 1. Clean OOP Design
- `AspectDetector`: Detection logic
- `AspectScorer`: Quality evaluation
- `DetectedAspect`: Data container
- Clear separation of concerns

### 2. Configurable Orbs
```python
from services.aspects.aspect_detector import AspectConfig, AspectType

custom_aspects = [
    AspectConfig(AspectType.CONJUNCTION, orb=10.0),  # Wider orb
    AspectConfig(AspectType.TRINE, orb=8.0)
]

detector = AspectDetector(aspect_configs=custom_aspects)
```

### 3. Strength Calculation
```
strength = 1.0 - (actual_orb / max_orb)

Examples:
- Exact conjunction (0° orb): strength = 1.0
- 4° orb with 8° max: strength = 0.5
- 8° orb with 8° max: strength = 0.0
```

### 4. Quality Scoring

| Aspect | Base Score | Nature |
|--------|-----------|---------|
| Trine | +1.0 | Harmonious |
| Sextile | +0.7 | Harmonious |
| Conjunction | Variable | Context-dependent |
| Opposition | -0.6 | Challenging |
| Square | -0.8 | Challenging |

**Conjunction Modifiers:**
- Sun-Moon: +1.0 (excellent)
- Venus-Mars: +0.9 (passionate)
- Mars-Mars: -0.5 (competitive)

## Algorithm Details

### Angular Distance Calculation
```python
def calculate_angular_distance(long1, long2):
    diff = abs(long1 - long2)
    if diff > 180:
        diff = 360 - diff  # Shortest path
    return diff
```

Handles wrap-around at 0°/360° boundary.

### Aspect Detection Logic
1. Calculate angular distance between planets
2. For each aspect type:
   - Check if distance ≈ aspect angle (within orb)
   - Calculate deviation from exact aspect
   - Compute strength score
3. Return strongest matching aspect

## Output Format

### Detected Aspect
```json
{
  "planet_a": "Sun",
  "planet_b": "Moon",
  "aspect": "Trine",
  "orb": 2.5,
  "exact_angle": 122.5,
  "strength": 0.58
}
```

### Synastry Aspect
```json
{
  "planet_a": "Venus (Person 1)",
  "planet_b": "Mars (Person 2)",
  "aspect": "Conjunction",
  "orb": 1.2,
  "exact_angle": 1.2,
  "strength": 0.85
}
```

## Testing

```bash
cd backend
python example_aspects.py
```

## Extension Points

### Add New Aspects
```python
class AspectType(Enum):
    QUINCUNX = 150
    SEMI_SEXTILE = 30
    SEMI_SQUARE = 45
```

### Custom Scoring Logic
Extend `AspectScorer` class:
```python
class CustomScorer(AspectScorer):
    def score_aspect(self, aspect):
        # Custom logic
        pass
```

### Planet-Specific Weights
Add to `CONJUNCTION_MODIFIERS` or create new scoring matrices.

## Next Steps

- [ ] Add minor aspects (quincunx, semi-square)
- [ ] Implement aspect patterns (Grand Trine, T-Square)
- [ ] Add applying vs separating aspect detection
- [ ] Support harmonic aspects
- [ ] Add aspect interpretation text generation

## Performance

- O(n²) for natal aspects (n = number of planets)
- O(n × m) for synastry (n, m = planets in each chart)
- Typical: ~10-20ms for 5 planets
- Optimized for real-time API responses
