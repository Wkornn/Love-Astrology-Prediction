# Birth Chart Calculator Module

## Overview

Production-grade birth chart calculation engine using Swiss Ephemeris.

## Architecture

```
services/
├── ephemeris/
│   ├── swisseph_adapter.py    # Low-level Swiss Ephemeris wrapper
│   └── planetary_calc.py      # High-level planetary position API
└── chart/
    ├── house_system.py         # House calculation (Placidus, etc.)
    └── birth_chart.py          # Main orchestration module
```

## Features

✅ Julian Day conversion  
✅ Planetary position calculation (Sun, Moon, Mercury, Venus, Mars)  
✅ House system calculation (Placidus)  
✅ Zodiac sign determination  
✅ House placement for planets  
✅ Clean JSON output  
✅ Comprehensive error handling  

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from app.services.chart.birth_chart import BirthChartCalculator

calculator = BirthChartCalculator()

result = calculator.calculate_chart_json(
    date='1990-01-15',
    time='14:30',
    latitude=40.7128,
    longitude=-74.0060,
    timezone='UTC'
)

print(result)
```

### Run Example Script

```bash
cd backend
python example_usage.py
```

## Output Format

```json
{
  "success": true,
  "data": {
    "planets": [
      {
        "name": "Sun",
        "sign": "Capricorn",
        "degree": 24.5,
        "house": 10,
        "longitude": 294.5
      },
      ...
    ],
    "houses": {
      "system": "Placidus",
      "cusps": [0.0, 30.5, 60.2, ...],
      "ascendant": {
        "sign": "Aries",
        "degree": 15.3,
        "longitude": 15.3
      },
      "midheaven": {
        "sign": "Capricorn",
        "degree": 5.2,
        "longitude": 275.2
      }
    },
    "birth_data": {
      "date": "1990-01-15",
      "time": "14:30",
      "latitude": 40.7128,
      "longitude": -74.006,
      "timezone": "UTC"
    }
  }
}
```

## Error Handling

All functions include comprehensive error handling:
- Invalid date/time formats
- Out-of-range coordinates
- Swiss Ephemeris calculation failures
- Missing ephemeris data files

## Next Steps

- [ ] Add timezone conversion support
- [ ] Implement aspect calculation
- [ ] Add more planets (Jupiter, Saturn, outer planets)
- [ ] Support additional house systems
- [ ] Add retrograde detection

## Testing

```bash
pytest tests/test_chart.py
```
