# Love Debugging Lab v2.0 - System Architecture

## Tech Stack

**Backend:** Python + FastAPI
- Astrology calculations: `swisseph` library
- Chart generation and aspect calculation
- Compatibility logic engine
- Humor generation system

**Frontend:** TypeScript + React/Vue
- User input forms
- Results visualization
- Responsive design

## Project Structure

```
Love-Astrology-Prediction/
├── backend/
│   ├── models.py              # Core data structures
│   ├── chart_calculator.py    # Natal chart calculations
│   ├── aspect_analyzer.py     # Aspect detection & scoring
│   ├── compatibility_engine.py # Compatibility logic
│   ├── humor_generator.py     # Bug reports & jokes
│   ├── api.py                 # FastAPI endpoints
│   └── requirements.txt
├── frontend/
│   ├── types.ts               # TypeScript interfaces
│   ├── components/
│   │   ├── BirthDataForm.tsx
│   │   ├── CompatibilityReport.tsx
│   │   └── BugList.tsx
│   └── api/
│       └── client.ts
└── README.md
```

## Module Responsibilities

### 1. Chart Calculator
- Input: BirthData
- Output: BirthChart
- Uses Swiss Ephemeris for accurate planetary positions

### 2. Aspect Analyzer
- Input: BirthChart(s)
- Output: List[Aspect]
- Detects planetary aspects with orb tolerance

### 3. Compatibility Engine
- Input: BirthChart (user1), BirthChart (user2)
- Output: CompatibilityResult
- Calculates scores based on synastry

### 4. Humor Generator
- Input: CompatibilityResult, Aspects
- Output: LoveBug[], forecast messages
- Engineering-themed jokes and warnings

## Data Flow

```
User Input (Birth Data)
    ↓
Chart Calculator → BirthChart
    ↓
Aspect Analyzer → Aspects
    ↓
Compatibility Engine → Scores
    ↓
Humor Generator → Bugs + Forecast
    ↓
Format Report → CompatibilityResult
    ↓
Return to Frontend
```

## Next Steps

1. ✅ Define core data structures
2. Implement chart calculator (swisseph wrapper)
3. Build aspect analyzer
4. Create compatibility scoring logic
5. Add humor generation
6. Build API endpoints
7. Create frontend UI
