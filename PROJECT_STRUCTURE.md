# Love Debugging Lab v2.0 - Project Structure (Refactored)

## Complete Folder Tree

```
Love-Astrology-Prediction/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI application entry point
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py                # Configuration management
│   │   │   └── models.py                # Core data structures
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ephemeris/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── swisseph_adapter.py  # Swiss Ephemeris wrapper
│   │   │   │   └── planetary_calc.py    # Planetary position calculations
│   │   │   │
│   │   │   ├── chart/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── birth_chart.py       # Natal chart generation
│   │   │   │   └── house_system.py      # House calculation (Placidus)
│   │   │   │
│   │   │   ├── aspects/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── aspect_detector.py   # Natal chart aspect detection
│   │   │   │   └── aspect_scorer.py     # Aspect quality scoring
│   │   │   │
│   │   │   ├── compatibility/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── scoring_engine.py    # Compatibility scoring (future)
│   │   │   │   └── archetype_matcher.py # Love archetype (future)
│   │   │   │
│   │   │   └── intelligence/
│   │   │       ├── __init__.py
│   │   │       ├── humor_generator.py   # Engineering-themed humor (future)
│   │   │       └── forecast_builder.py  # Forecast generation (future)
│   │   │
│   │   ├── rules/
│   │   │   ├── __init__.py
│   │   │   ├── aspect_rules.json        # Aspect interpretation rules
│   │   │   ├── compatibility_rules.json # Compatibility scoring rules
│   │   │   └── humor_templates.json     # Bug report templates
│   │   │
│   │   ├── reports/
│   │   │   ├── __init__.py
│   │   │   ├── report_generator.py      # Report assembly (future)
│   │   │   └── formatters.py            # Output formatting (future)
│   │   │
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── routes/
│   │       │   ├── __init__.py
│   │       │   ├── chart.py             # Chart calculation endpoints
│   │       │   └── health.py            # Health check endpoints
│   │       │
│   │       └── schemas/
│   │           ├── __init__.py
│   │           ├── requests.py          # API request models
│   │           └── responses.py         # API response models
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_chart.py
│   │   ├── test_aspects.py
│   │   └── fixtures/
│   │       └── sample_charts.json
│   │
│   ├── example_usage.py                 # Birth chart example
│   ├── example_aspects.py               # Aspect detection example
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── types/
│   │   │   └── index.ts                 # TypeScript type definitions
│   │   │
│   │   ├── api/
│   │   │   └── client.ts                # API client
│   │   │
│   │   ├── components/
│   │   │   ├── BirthDataForm.tsx        # User input form
│   │   │   ├── ChartDisplay.tsx         # Chart visualization
│   │   │   └── AspectList.tsx           # Aspect display
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   └── tsconfig.json
│
├── data/
│   └── ephemeris/                       # Swiss Ephemeris data files
│
├── docs/
│   ├── API.md                           # API documentation
│   ├── ARCHITECTURE.md                  # System architecture
│   ├── PROJECT_STRUCTURE.md             # This file
│   └── ASPECT_ENGINE.md                 # Aspect engine docs
│
├── types.ts                             # Shared TypeScript types
├── models.py                            # Legacy (moved to backend/app/core/)
├── .gitignore
└── README.md
```

---

## What Changed (Refactoring Summary)

### ❌ **REMOVED**
1. **Synastry Service** (`services/synastry/`)
   - `synastry_engine.py` - Cross-chart aspect analysis
   - `composite_chart.py` - Composite chart generation
   
2. **Synastry Logic in Aspect Engine**
   - `detect_synastry_aspects()` method removed
   - Dual-mode detection simplified to natal-only
   - Person 1/Person 2 labeling removed

3. **API Routes**
   - `routes/compatibility.py` - Removed (was for synastry)

### ✅ **KEPT & SIMPLIFIED**
1. **Aspect Detector** (`aspect_detector.py`)
   - Now: Single method `detect_aspects()` for natal charts
   - Removed: `detect_synastry_aspects()` and dual-mode logic
   - Cleaner interface, single responsibility

2. **Aspect Scorer** (`aspect_scorer.py`)
   - Removed synastry-specific planet name parsing
   - Kept quality scoring logic (harmonious/challenging)
   - Still extensible for future use

3. **Core Services**
   - Birth chart calculation (unchanged)
   - House system (unchanged)
   - Ephemeris adapter (unchanged)

### 🔧 **UPDATED**
1. **Documentation**
   - All docstrings updated to reflect natal-only scope
   - Added "Future extension point" notes for synastry
   - Removed synastry examples from docs

2. **Example Scripts**
   - `example_aspects.py` - Now shows only natal aspects
   - Removed synastry demonstration code

---

## Module Responsibilities (Updated)

### **Ephemeris Service** (`services/ephemeris/`)
- Swiss Ephemeris wrapper
- Planetary position calculations
- Julian Day conversion

### **Chart Service** (`services/chart/`)
- Natal chart generation
- House system calculation
- Planet house placement

### **Aspects Service** (`services/aspects/`)
- **Natal chart aspect detection only**
- Aspect quality scoring
- Strength calculation

### **Compatibility Service** (`services/compatibility/`) - FUTURE
- Will handle love compatibility scoring
- Archetype matching
- Uses natal chart + aspects as input

### **Intelligence Layer** (`services/intelligence/`) - FUTURE
- Humor generation (engineering-themed bugs)
- Relationship forecast
- Report narrative

---

## Design Rationale

### Why Remove Synastry Now?

1. **Scope Clarity**: Focus on single-user natal chart analysis first
2. **Simpler Architecture**: Easier to understand and maintain
3. **Faster Development**: Build compatibility logic without cross-chart complexity
4. **Better Testing**: Isolated natal chart logic is easier to test

### Extension Points for Future Synastry

When synastry is needed, add:

```python
# Future: services/synastry/synastry_engine.py
class SynastryEngine:
    def __init__(self, aspect_detector: AspectDetector):
        self.detector = aspect_detector
    
    def analyze_compatibility(self, chart1, chart2):
        # Cross-chart aspect detection
        # Use existing AspectDetector for individual aspects
        pass
```

**Key Design Principle**: AspectDetector remains focused on detecting aspects between any two planetary positions. Synastry logic will orchestrate multiple calls to AspectDetector.

---

## Current Data Flow

```
User Input (Birth Data)
    ↓
Chart Calculator → BirthChart
    ↓
Aspect Detector → Natal Aspects
    ↓
Aspect Scorer → Quality Scores
    ↓
[Future: Compatibility Engine] → Scores + Archetype
    ↓
[Future: Humor Generator] → Bugs + Forecast
    ↓
[Future: Report Generator] → Final Report
```

---

## Next Implementation Steps

1. ✅ Birth chart calculation
2. ✅ Aspect detection (natal only)
3. ⏳ Compatibility scoring engine (single chart personality analysis)
4. ⏳ Humor intelligence layer
5. ⏳ Report generation
6. ⏳ API endpoints
7. ⏳ Frontend UI
8. 🔮 Future: Synastry re-introduction

---

## Benefits of This Refactoring

✅ **Cleaner Code**: Single responsibility per module  
✅ **Easier Testing**: No cross-chart complexity  
✅ **Faster Development**: Focus on core features first  
✅ **Better Documentation**: Clear scope boundaries  
✅ **Extensible**: Easy to add synastry later without refactoring  

---

**Architecture is now streamlined for natal chart analysis with clear extension points for future synastry features.**
